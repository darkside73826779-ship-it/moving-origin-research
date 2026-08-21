#!/usr/bin/env python3
"""Deterministic base..tip workflow preflight report generator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


TOOL_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOL_ROOT
PATTERNS = TOOL_ROOT / "specs/data/workflow_preflight_patterns_v1.json"
SCHEMA = TOOL_ROOT / "specs/data/workflow_preflight_report_schema_v2.json"
SHA_RE = re.compile(r"[0-9a-f]{40}")
STATUS_MAP = {"A": "added", "M": "modified", "D": "deleted", "R100": "renamed", "T": "type_changed"}


class PreflightError(RuntimeError):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


def configure_root(repo_root: str | Path) -> None:
    """Select the explicit repository whose Git objects and output are governed."""
    global ROOT
    candidate = Path(repo_root).resolve(strict=False)
    probe = subprocess.run(
        ["git", "-C", str(candidate), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
    )
    if probe.returncode or Path(probe.stdout.strip()).resolve(strict=False) != candidate:
        raise PreflightError("repo root is not an exact Git worktree root", 4)
    ROOT = candidate


def _git(*args: str, binary: bool = False, check: bool = True) -> subprocess.CompletedProcess[Any]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, encoding=None if binary else "utf-8", errors=None if binary else "strict",
    )
    if check and result.returncode:
        error = result.stderr.decode("utf-8", "replace") if binary else result.stderr
        raise PreflightError(f"git command failed: {' '.join(args)}: {error.strip()}", 4)
    return result


def canonical_bytes(value: Any) -> bytes:
    # The report domain has no floating-point values; RFC 8785 therefore equals
    # compact, Unicode-preserving, lexicographically keyed JSON.
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value: str) -> bool:
    return SHA_RE.fullmatch(value) is not None


def _object(commit: str, path: str) -> tuple[str, str | None, bytes | None]:
    raw = _git("ls-tree", "-z", commit, "--", path, binary=True).stdout
    if not raw:
        return "deleted", None, None
    header, listed = raw[:-1].split(b"\t", 1)
    if listed.decode("utf-8", "strict") != path:
        raise PreflightError("ls-tree path mismatch", 5)
    mode, kind, oid = header.decode("ascii").split()
    if kind == "commit" or mode == "160000":
        raise PreflightError("submodules are prohibited", 5)
    if kind != "blob" or mode not in {"100644", "100755", "120000"}:
        raise PreflightError("unsupported Git object type", 5)
    content = _git("cat-file", "blob", oid, binary=True).stdout
    return ("symlink" if mode == "120000" else "regular"), hashlib.sha256(content).hexdigest(), content


def _events(old: str, new: str, domain: str) -> list[dict[str, Any]]:
    raw = _git("diff-tree", "-r", "--raw", "-z", "--no-commit-id", "--find-renames=100%", old, new, binary=True).stdout
    tokens = raw.split(b"\0")
    events: list[dict[str, Any]] = []
    i = 0
    while i < len(tokens) and tokens[i]:
        header = tokens[i]
        i += 1
        if b"\t" in header:
            metadata, first_path = header.split(b"\t", 1)
        else:
            metadata = header
            if i >= len(tokens):
                raise PreflightError("malformed raw diff", 5)
            first_path = tokens[i]
            i += 1
        try:
            fields = metadata.decode("ascii").split()
            status = fields[4]
            path1 = first_path.decode("utf-8", "strict")
        except (IndexError, UnicodeError) as exc:
            raise PreflightError("malformed or non-UTF-8 raw diff", 5) from exc
        if status not in STATUS_MAP:
            raise PreflightError(f"unsupported diff status {status}", 5)
        old_path = None
        path = path1
        if status == "R100":
            if i >= len(tokens):
                raise PreflightError("malformed rename", 5)
            old_path, path = path1, tokens[i].decode("utf-8", "strict")
            i += 1
        object_type, digest, _ = _object(new, path) if status != "D" else ("deleted", None, None)
        events.append({
            "domain_id": domain, "old_path": old_path, "path": path,
            "change_type": STATUS_MAP[status], "object_type": object_type, "sha256": digest,
        })
    events.sort(key=lambda row: (
        row["path"].encode("utf-8"), b"" if row["old_path"] is None else row["old_path"].encode("utf-8"), row["change_type"]
    ))
    return events


def _added_patch(old: str, new: str) -> bytes:
    raw = _git("diff", "--no-ext-diff", "--no-color", "--unified=0", old, new, binary=True).stdout
    return b"".join(
        line[1:]
        for line in raw.splitlines(keepends=True)
        if line.startswith(b"+") and not line.startswith(b"+++")
    )


def _scan_units(old: str, new: str, events: list[dict[str, Any]]) -> list[tuple[str | None, bytes]]:
    units: list[tuple[str | None, bytes]] = [(None, _added_patch(old, new))]
    for event in events:
        if event["object_type"] != "deleted":
            _, _, content = _object(new, event["path"])
            assert content is not None
            units.append((event["path"], content))
    return units


def _line_column(data: bytes, start: int) -> tuple[int, int]:
    prefix = data[:start]
    return prefix.count(b"\n") + 1, start - prefix.rfind(b"\n")


def _definition_literal(text: str, start: int, end: int, klass: str) -> bool:
    for match in re.finditer(r'\{"class":"([^"\\]+)","pattern":"', text):
        if match.group(1) != klass:
            continue
        pos = match.end()
        escaped = False
        while pos < len(text):
            char = text[pos]
            if char == '"' and not escaped:
                break
            if char == "\\" and not escaped:
                escaped = True
            else:
                escaped = False
            pos += 1
        if match.end() <= start and end <= pos:
            return True
    return False


def _fixed_findings(domain: str, units: Iterable[tuple[str | None, bytes]], patterns: list[dict[str, str]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    compiled = [(item["class"], re.compile(item["pattern"], re.ASCII | re.MULTILINE)) for item in patterns]
    for path, data in units:
        text = data.decode("utf-8", "replace")
        for klass, regex in compiled:
            for match in regex.finditer(text):
                evidence = match.group(0).encode("utf-8")
                encoded_prefix = text[:match.start()].encode("utf-8")
                line, column = _line_column(data, len(encoded_prefix))
                literal = path == "specs/data/workflow_preflight_patterns_v1.json" and _definition_literal(text, match.start(), match.end(), klass)
                findings.append({
                    "scan_domain_ids": [domain], "detector": "fixed_regex", "class": klass,
                    "path": path, "line": line, "column": column,
                    "evidence_sha256": hashlib.sha256(evidence).hexdigest(),
                    "context_kind": "SCANNER_DEFINITION_LITERAL" if literal else "CONTENT",
                    "disposition": "REBECCA_DECISION" if literal else "BLOCKER",
                    "rationale_code": "SCANNER_PATTERN_SELF_MATCH" if literal else "PROHIBITED_CONTENT_MATCH",
                })
    return findings


def _gitleaks(domain: str, units: list[tuple[str | None, bytes]]) -> tuple[str, int, list[dict[str, Any]]]:
    executable = shutil.which("gitleaks")
    if executable is None:
        raise PreflightError("gitleaks is unavailable", 3)
    version_result = subprocess.run([executable, "version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if version_result.returncode or not version_result.stdout.strip():
        raise PreflightError("gitleaks version failed", 3)
    payload = b"\n".join(data for _, data in units)
    with tempfile.TemporaryDirectory(prefix="mor-preflight-") as temporary:
        report = Path(temporary) / "gitleaks.json"
        result = subprocess.run(
            [executable, "stdin", "--no-banner", "--no-color", "--report-format", "json", "--report-path", str(report)],
            input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode not in {0, 1}:
            raise PreflightError("gitleaks scanner error", 3)
        try:
            records = json.loads(report.read_text(encoding="utf-8")) if report.exists() and report.stat().st_size else []
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise PreflightError("invalid gitleaks report", 3) from exc
    findings: list[dict[str, Any]] = []
    for record in records:
        secret_field = "Sec" + "ret"
        detected_value = record.get(secret_field)
        if not isinstance(detected_value, str):
            raise PreflightError(f"gitleaks finding lacks {secret_field} field", 3)
        line = record.get("StartLine") if isinstance(record.get("StartLine"), int) and record["StartLine"] >= 1 else None
        column = record.get("StartColumn") if isinstance(record.get("StartColumn"), int) and record["StartColumn"] >= 1 else None
        findings.append({
            "scan_domain_ids": [domain], "detector": "gitleaks", "class": "credentials",
            "path": None, "line": line, "column": column,
            "evidence_sha256": hashlib.sha256(detected_value.encode("utf-8")).hexdigest(),
            "context_kind": "CONTENT", "disposition": "BLOCKER", "rationale_code": "PROHIBITED_CONTENT_MATCH",
        })
    return version_result.stdout.strip(), result.returncode, findings


def _deduplicate(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ("detector", "class", "path", "line", "column", "evidence_sha256", "context_kind", "disposition", "rationale_code")
    reduced: dict[tuple[Any, ...], dict[str, Any]] = {}
    for finding in findings:
        key = tuple(finding[name] for name in keys)
        if key not in reduced:
            reduced[key] = dict(finding)
        else:
            reduced[key]["scan_domain_ids"].extend(finding["scan_domain_ids"])
    for finding in reduced.values():
        finding["scan_domain_ids"] = sorted(set(finding["scan_domain_ids"]), key=lambda value: value.encode("utf-8"))
    values = list(reduced.values())
    values.sort(key=lambda item: (
        (1, b"") if item["path"] is None else (0, item["path"].encode("utf-8")),
        (1, 0) if item["line"] is None else (0, item["line"]),
        (1, 0) if item["column"] is None else (0, item["column"]),
        item["detector"], item["class"], item["evidence_sha256"], item["context_kind"],
        item["disposition"], item["rationale_code"], "\0".join(item["scan_domain_ids"]),
    ))
    for index, finding in enumerate(values, 1):
        finding["finding_id"] = f"F{index:06d}"
    return values


def _schema_check(value: Any, rule: dict[str, Any], root: dict[str, Any], location: str = "$") -> None:
    if "$ref" in rule:
        ref = rule["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise PreflightError(f"unsupported schema reference at {location}", 5)
        target: Any = root
        for token in ref[2:].split("/"):
            target = target[token.replace("~1", "/").replace("~0", "~")]
        _schema_check(value, target, root, location)
        return
    if "anyOf" in rule:
        for alternative in rule["anyOf"]:
            try:
                _schema_check(value, alternative, root, location)
                break
            except PreflightError:
                pass
        else:
            raise PreflightError(f"schema anyOf mismatch at {location}", 5)
    if "const" in rule and value != rule["const"]:
        raise PreflightError(f"schema const mismatch at {location}", 5)
    if "enum" in rule and value not in rule["enum"]:
        raise PreflightError(f"schema enum mismatch at {location}", 5)
    if "type" in rule:
        names = rule["type"] if isinstance(rule["type"], list) else [rule["type"]]
        matches = {
            "object": isinstance(value, dict), "array": isinstance(value, list),
            "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool),
            "boolean": isinstance(value, bool), "null": value is None,
        }
        if not any(matches.get(name, False) for name in names):
            raise PreflightError(f"schema type mismatch at {location}", 5)
    if isinstance(value, dict):
        required = set(rule.get("required", []))
        if not required.issubset(value):
            raise PreflightError(f"schema required member missing at {location}", 5)
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False and not set(value).issubset(properties):
            raise PreflightError(f"schema unknown member at {location}", 5)
        for name, child in value.items():
            if name in properties:
                _schema_check(child, properties[name], root, f"{location}.{name}")
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0) or ("maxItems" in rule and len(value) > rule["maxItems"]):
            raise PreflightError(f"schema array length mismatch at {location}", 5)
        if rule.get("uniqueItems") and len({_canonical_key(item) for item in value}) != len(value):
            raise PreflightError(f"schema duplicate array member at {location}", 5)
        if "items" in rule:
            for index, child in enumerate(value):
                _schema_check(child, rule["items"], root, f"{location}[{index}]")
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0) or ("pattern" in rule and re.search(rule["pattern"], value) is None):
            raise PreflightError(f"schema string mismatch at {location}", 5)
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in rule and value < rule["minimum"]:
        raise PreflightError(f"schema integer mismatch at {location}", 5)
    for conditional in rule.get("allOf", []):
        condition = conditional.get("if")
        if condition is None:
            _schema_check(value, conditional, root, location)
            continue
        try:
            _schema_check(value, condition, root, location)
        except PreflightError:
            branch = conditional.get("else")
        else:
            branch = conditional.get("then")
        if branch is not None:
            _schema_check(value, branch, root, location)


def _canonical_key(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _validate_report(report: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    _schema_check(report, schema, schema)
    if [item["event_index"] for item in report["path_events"]] != list(range(1, len(report["path_events"]) + 1)):
        raise PreflightError("event indexes are not contiguous", 5)


def build_report(base: str, tip: str) -> tuple[dict[str, Any], int]:
    if not _sha(base) or not _sha(tip) or base == tip:
        raise PreflightError("base/tip must be distinct lowercase 40-hex SHAs", 4)
    for value in (base, tip):
        _git("cat-file", "-e", f"{value}^{{commit}}")
    if _git("merge-base", "--is-ancestor", base, tip, check=False).returncode != 0:
        raise PreflightError("base is not an ancestor of tip", 4)
    commits = [line for line in _git("rev-list", "--reverse", "--topo-order", f"{base}..{tip}").stdout.splitlines() if line]
    introduced: list[dict[str, Any]] = []
    domains: list[tuple[dict[str, str], str, str]] = []
    for commit in commits:
        parents = _git("show", "-s", "--format=%P", commit).stdout.strip().split()
        if not parents:
            raise PreflightError("root commit in introduced range", 5)
        introduced.append({"sha": commit, "parent_shas": parents, "is_merge": len(parents) > 1})
        for parent in parents:
            domain_id = f"C:{commit}:P:{parent}"
            domains.append(({"domain_id": domain_id, "kind": "commit_parent", "old_sha": parent, "new_sha": commit}, parent, commit))
    combined_id = f"R:{base}:{tip}"
    domains.append(({"domain_id": combined_id, "kind": "combined_base_tip", "old_sha": base, "new_sha": tip}, base, tip))

    pattern_document = json.loads(PATTERNS.read_text(encoding="utf-8"))
    if pattern_document.get("engine") != "python-re-ascii-multiline" or pattern_document.get("finding_policy") != "any_match_blocks":
        raise PreflightError("pattern contract mismatch", 5)
    path_events: list[dict[str, Any]] = []
    combined_events: list[dict[str, Any]] = []
    raw_findings: list[dict[str, Any]] = []
    versions: set[str] = set()
    gitleaks_exit = 0
    for domain, old, new in domains:
        events = _events(old, new, domain["domain_id"])
        path_events.extend(events)
        if domain["domain_id"] == combined_id:
            combined_events = events
        units = _scan_units(old, new, events)
        raw_findings.extend(_fixed_findings(domain["domain_id"], units, pattern_document["patterns"]))
        version, exit_code, scanner_findings = _gitleaks(domain["domain_id"], units)
        versions.add(version)
        gitleaks_exit = max(gitleaks_exit, exit_code)
        raw_findings.extend(scanner_findings)
    for index, event in enumerate(path_events, 1):
        event["event_index"] = index
    findings = _deduplicate(raw_findings)
    blocked = bool(findings)
    report = {
        "schema_version": "workflow-preflight-report-v2", "base_sha": base, "tip_sha": tip,
        "base_is_ancestor": True, "merge_policy": "scan_each_commit_against_each_parent_and_scan_combined_base_tip",
        "scan_domains": [item[0] for item in domains], "introduced_commits": introduced,
        "path_events": path_events,
        "paths": [{key: event[key] for key in ("old_path", "path", "change_type", "object_type", "sha256")} for event in combined_events],
        "secret_scanner": {"tool": "gitleaks", "version": ",".join(sorted(versions)), "exit_code": gitleaks_exit,
                           "finding_count": sum(item["detector"] == "gitleaks" for item in findings)},
        "findings": findings, "canonicalization": "rfc8785_utf8_no_bom_single_lf_sidecar_raw_sha256",
        "manual_review_required": True, "status": "BLOCKED" if blocked else "CLEAN",
    }
    _validate_report(report)
    return report, 2 if blocked else 0


def write_report(report: dict[str, Any], output: str) -> None:
    path = Path(output)
    if path.is_absolute() or ".." in path.parts or str(path) in {"", "."}:
        raise PreflightError("output must be repository-relative", 5)
    destination = (ROOT / path).resolve(strict=False)
    try:
        destination.relative_to(ROOT)
    except ValueError as exc:
        raise PreflightError("output escapes repository", 5) from exc
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(report) + b"\n"
    destination.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    sidecar = destination.with_name(destination.name + ".sha256")
    sidecar.write_bytes(f"{digest}  {destination.name}\n".encode("ascii"))
    if destination.read_bytes() != raw or sidecar.read_bytes() != f"{digest}  {destination.name}\n".encode("ascii"):
        raise PreflightError("output digest verification failed", 5)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--base", required=True)
    parser.add_argument("--tip", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        configure_root(args.repo_root)
        report, code = build_report(args.base, args.tip)
        write_report(report, args.output)
        print(
            f"{report['status']}: findings={len(report['findings'])} "
            f"report={args.output} repo={ROOT}",
            file=sys.stderr if code else sys.stdout,
        )
        return code
    except PreflightError as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return exc.code
    except (OSError, UnicodeError, json.JSONDecodeError, re.error) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
