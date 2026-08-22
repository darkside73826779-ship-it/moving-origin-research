#!/usr/bin/env python3
"""Prepare and optionally publish a canonical role-return topology.

The helper deliberately uses Git plumbing until every commit and check is
complete.  A failure therefore leaves the caller's branch and index intact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any


TOOL_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = TOOL_ROOT / "tools/workflow_preflight.py"
VALIDATOR = TOOL_ROOT / "tools/workflow_contract_validator.py"
SHA = re.compile(r"^[0-9a-f]{40}$")
BRANCH = re.compile(r"^(architect|critic|taskbuilder|integrator|recorder|judge|coordinator)/[A-Za-z0-9._/-]+$")


class Stop(RuntimeError):
    pass


def _run(argv: list[str], *, cwd: Path, binary: bool = False, check: bool = True,
         env: dict[str, str] | None = None) -> subprocess.CompletedProcess[Any]:
    result = subprocess.run(
        argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, encoding=None if binary else "utf-8", env=env,
    )
    if check and result.returncode:
        stderr = result.stderr.decode("utf-8", "replace") if binary else result.stderr
        raise Stop(f"command failed ({' '.join(argv)}): {stderr.strip()}")
    return result


def _git(repo: Path, *args: str, binary: bool = False, check: bool = True,
         env: dict[str, str] | None = None) -> subprocess.CompletedProcess[Any]:
    return _run(["git", *args], cwd=repo, binary=binary, check=check, env=env)


def _oid(repo: Path, value: str) -> str:
    oid = _git(repo, "rev-parse", "--verify", f"{value}^{{commit}}").stdout.strip()
    if not SHA.fullmatch(oid):
        raise Stop(f"invalid commit identity: {value}")
    return oid


def _repo_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or not value or value.startswith("/"):
        raise Stop(f"invalid repository path: {value}")
    return path.as_posix()


def _outside(repo: Path, value: str, *, must_exist: bool = True) -> Path:
    path = Path(value).resolve(strict=must_exist)
    try:
        path.relative_to(repo)
    except ValueError:
        return path
    raise Stop("handoff/template/classification files must be outside the repository")


def _remote_oid(repo: Path, remote: str, branch: str) -> str | None:
    ref = f"refs/heads/{branch}"
    rows = _git(repo, "ls-remote", "--refs", remote, ref).stdout.splitlines()
    if not rows:
        return None
    if len(rows) != 1:
        raise Stop(f"remote ref is non-unique: {ref}")
    oid, found = rows[0].split("\t")
    if found != ref or not SHA.fullmatch(oid):
        raise Stop(f"malformed remote ref result: {ref}")
    return oid


def _commit(repo: Path, tree: str, parent: str, message: str, commit_date: str) -> str:
    if not message.strip() or "\x00" in message:
        raise Stop("commit message is empty or invalid")
    environment = {**os.environ, "GIT_EDITOR": "true", "GIT_AUTHOR_DATE": commit_date,
                   "GIT_COMMITTER_DATE": commit_date}
    result = subprocess.run(
        ["git", "commit-tree", tree, "-p", parent], cwd=repo,
        input=(message.rstrip() + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment,
    )
    if result.returncode:
        raise Stop(f"commit-tree failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    oid = result.stdout.decode("ascii").strip()
    if not SHA.fullmatch(oid):
        raise Stop("commit-tree returned an invalid identity")
    return oid


def _tree_with_file(repo: Path, parent: str, path: str, content: bytes) -> str:
    with tempfile.NamedTemporaryFile(prefix="mor-return-index-", delete=False) as handle:
        index = Path(handle.name)
    index.unlink(missing_ok=True)
    env = {**os.environ, "GIT_INDEX_FILE": str(index)}
    try:
        _git(repo, "read-tree", f"{parent}^{{tree}}", env=env)
        blob = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"], cwd=repo, input=content,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if blob.returncode:
            raise Stop(f"hash-object failed: {blob.stderr.decode('utf-8', 'replace').strip()}")
        oid = blob.stdout.decode("ascii").strip()
        _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{oid},{path}", env=env)
        return _git(repo, "write-tree", env=env).stdout.strip()
    finally:
        index.unlink(missing_ok=True)


def _changed(repo: Path, base: str, tip: str) -> list[tuple[str, str]]:
    raw = _git(repo, "diff", "--name-status", "-z", "--no-renames", base, tip, binary=True).stdout
    tokens = raw.split(b"\0")
    rows: list[tuple[str, str]] = []
    for index in range(0, len(tokens) - 1, 2):
        if not tokens[index]:
            break
        status = tokens[index].decode("ascii")
        path = tokens[index + 1].decode("utf-8")
        if status not in {"A", "M", "D", "T"}:
            raise Stop(f"unsupported change status: {status}")
        rows.append((status, path))
    return rows


def _named_paths(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"artifacts", "remote_ref", "work_branch"}:
                continue
            if key in {"path", "ruling_path", "source_trace_path", "specification_path"} and isinstance(child, str):
                found.add(_repo_path(child))
            elif key.endswith("_paths") and isinstance(child, list):
                found.update(_repo_path(path) for path in child)
            else:
                found.update(_named_paths(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_named_paths(child))
    return found


def _inventory(repo: Path, base: str, routing: str, named_paths: set[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for status, path in _changed(repo, base, routing):
        if status == "D":
            raise Stop("deleted artifacts cannot be represented by manifest v1")
        raw = _git(repo, "show", f"{routing}:{path}", binary=True).stdout
        result[path] = hashlib.sha256(raw).hexdigest()
    for path in sorted(named_paths, key=lambda item: item.encode("utf-8")):
        raw = _git(repo, "show", f"{routing}:{path}", binary=True).stdout
        result[path] = hashlib.sha256(raw).hexdigest()
    if not result:
        raise Stop("artifact inventory is empty")
    return dict(sorted(result.items(), key=lambda row: row[0].encode("utf-8")))


def _load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise Stop(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_preflight(repo: Path, base: str, tip: str, label: str) -> tuple[dict[str, Any], str]:
    temporary = f".workflow-return-{uuid.uuid4().hex}-{label}.json"
    try:
        result = _run(
            [sys.executable, str(PREFLIGHT), "--repo-root", str(repo), "--base", base,
             "--tip", tip, "--output", temporary], cwd=repo, check=False,
        )
        if result.returncode not in {0, 2}:
            raise Stop(f"{label} preflight failed: {result.stderr.strip()}")
        raw = (repo / temporary).read_bytes()
        report = json.loads(raw.decode("utf-8"))
        return report, hashlib.sha256(raw).hexdigest()
    finally:
        (repo / temporary).unlink(missing_ok=True)
        (repo / f"{temporary}.sha256").unlink(missing_ok=True)


def _finding_id(scope: str, finding: dict[str, Any]) -> str:
    raw = json.dumps(finding, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(scope.encode("ascii") + b"\0" + raw).hexdigest()


def _classification_template(path: Path, reports: list[tuple[str, dict[str, Any], str]]) -> None:
    rows = []
    for scope, report, _ in reports:
        for finding in report["findings"]:
            rows.append({
                "finding_id": _finding_id(scope, finding), "scope": scope,
                "detector": finding["detector"], "class": finding["class"],
                "disposition": "UNCLASSIFIED", "rationale": "",
            })
    document = {
        "schema_version": "workflow-return-manual-classifications-v1",
        "reports": {scope: digest for scope, _, digest in reports},
        "classifications": rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n")


def _validate_classifications(path: Path, reports: list[tuple[str, dict[str, Any], str]]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != "workflow-return-manual-classifications-v1":
        raise Stop("classification document identity mismatch")
    expected_reports = {scope: digest for scope, _, digest in reports}
    if value.get("reports") != expected_reports:
        raise Stop("classification report identities mismatch")
    expected = {
        _finding_id(scope, finding): (scope, finding["detector"], finding["class"])
        for scope, report, _ in reports for finding in report["findings"]
    }
    rows = value.get("classifications")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise Stop("classification rows are incomplete")
    seen: set[str] = set()
    allowed = {"ACCEPTABLE_IMMUTABLE_IDENTITY", "ACCEPTABLE_PUBLIC_DIGEST"}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"finding_id", "scope", "detector", "class", "disposition", "rationale"}:
            raise Stop("classification row shape mismatch")
        finding_id = row["finding_id"]
        identity = expected.get(finding_id)
        if (finding_id in seen or identity is None
                or identity != (row["scope"], row["detector"], row["class"])):
            raise Stop("classification finding identity mismatch")
        if row["disposition"] not in allowed or not isinstance(row["rationale"], str) or not row["rationale"].strip():
            raise Stop("finding is not explicitly and acceptably classified")
        seen.add(finding_id)
    if seen != set(expected):
        raise Stop("classification coverage mismatch")


def _assert_routing_only(repo: Path, result: str, routing: str, handoff_path: str) -> None:
    if _changed(repo, result, routing) != [("A", handoff_path)]:
        raise Stop("routing tail is not an exact handoff-only commit")


def _assert_manifest_only(repo: Path, routing: str, manifest: str, manifest_path: str) -> None:
    if _changed(repo, routing, manifest) != [("A", manifest_path)]:
        raise Stop("manifest branch changes package bytes")


def _push(repo: Path, remote: str, branches: dict[str, str]) -> None:
    refspecs = [f"{oid}:refs/heads/{branch}" for branch, oid in branches.items()]
    command = ["git", "push", "--atomic", remote, *refspecs]
    if any("force" in item.lower() for item in command):
        raise Stop("force-push is prohibited")
    _run(command, cwd=repo)
    for branch, oid in branches.items():
        if _remote_oid(repo, remote, branch) != oid:
            raise Stop(f"remote equality failed: {branch}")


def _install_refs(repo: Path, result_branch: str, result: str, base: str,
                  routing_branch: str, routing: str, manifest_branch: str, manifest: str) -> None:
    transaction = (
        "start\n"
        f"update refs/heads/{result_branch} {result} {base}\n"
        f"update refs/heads/{routing_branch} {routing} {'0' * 40}\n"
        f"update refs/heads/{manifest_branch} {manifest} {'0' * 40}\n"
        "prepare\ncommit\n"
    ).encode("ascii")
    result_process = subprocess.run(
        ["git", "update-ref", "--stdin"], cwd=repo, input=transaction,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result_process.returncode:
        raise Stop(f"atomic ref installation failed: {result_process.stderr.decode('utf-8', 'replace').strip()}")


def publish(args: argparse.Namespace) -> dict[str, str]:
    repo = Path(args.repo_root).resolve(strict=True)
    top = Path(_git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if top != repo:
        raise Stop("repo-root must be the exact worktree root")
    for branch in (args.result_branch, args.routing_branch, args.manifest_branch, args.work_branch):
        if not BRANCH.fullmatch(branch):
            raise Stop(f"invalid governed branch: {branch}")
    if len({args.result_branch, args.routing_branch, args.manifest_branch}) != 3:
        raise Stop("result, routing, and manifest branches must be distinct")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})", args.commit_date):
        raise Stop("commit-date must be an exact RFC 3339 second")
    current = _git(repo, "branch", "--show-current").stdout.strip()
    if current != args.result_branch:
        raise Stop("current branch does not equal result-branch")
    base = _oid(repo, args.base)
    if _oid(repo, "HEAD") != base:
        raise Stop("HEAD must equal the exact base before preparation")
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    staged = [line[3:] for line in status if line[:1] not in {" ", "?"}]
    if not staged or any(line[:1] in {" ", "?"} or line[1:2] != " " for line in status):
        raise Stop("require staged package changes only; unstaged/untracked changes are prohibited")
    handoff_path = _repo_path(args.handoff_path)
    manifest_path = _repo_path(args.manifest_path)
    if not handoff_path.startswith("handoffs/") or not manifest_path.startswith("handoffs/"):
        raise Stop("handoff and manifest destinations must be under handoffs/")
    if any(path.startswith("handoffs/") for path in staged):
        raise Stop("substantive result may not stage handoff artifacts")
    handoff_source = _outside(repo, args.handoff_source)
    template_source = _outside(repo, args.manifest_template)
    classification = _outside(repo, args.classification_template, must_exist=False)
    for branch in (args.routing_branch, args.manifest_branch):
        if _git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False).returncode == 0:
            raise Stop(f"local branch already exists: {branch}")
    remote_result = _remote_oid(repo, args.remote, args.result_branch)
    if remote_result not in {None, base}:
        raise Stop("remote result branch is not absent or equal to base")
    if _remote_oid(repo, args.remote, args.routing_branch) is not None or _remote_oid(repo, args.remote, args.manifest_branch) is not None:
        raise Stop("routing/manifest remote branch already exists")

    temp_prefix = f"refs/mor/return/{uuid.uuid4().hex}"
    temp_refs: list[str] = []
    try:
        result_tree = _git(repo, "write-tree").stdout.strip()
        result = _commit(repo, result_tree, base, args.result_message, args.commit_date)
        result_ref = f"{temp_prefix}/result"; _git(repo, "update-ref", result_ref, result); temp_refs.append(result_ref)
        routing_tree = _tree_with_file(repo, result, handoff_path, handoff_source.read_bytes())
        routing = _commit(repo, routing_tree, result, args.routing_message, args.commit_date)
        routing_ref = f"{temp_prefix}/routing"; _git(repo, "update-ref", routing_ref, routing); temp_refs.append(routing_ref)
        _assert_routing_only(repo, result, routing, handoff_path)

        # The substantive domain includes its handoff-only routing tail so no
        # return text can reach a remote ref without a scan.
        substantive_report, substantive_digest = run_preflight(repo, base, routing, "substantive")
        template = json.loads(template_source.read_text(encoding="utf-8"))
        template.update({
            "remote_ref": f"refs/heads/{args.routing_branch}", "base_sha": base,
            "routing_ref_sha": routing, "review_result_sha": result,
            "work_branch": args.work_branch,
            "scan_attestation": {
                "base_sha": base, "tip_sha": routing,
                "tool_status": substantive_report["status"].lower(),
                "manual_review": bool(args.manual_review),
                "findings": [_finding_id("substantive", row) for row in substantive_report["findings"]],
            },
        })
        template["artifacts"] = _inventory(repo, base, routing, _named_paths(template))
        validator = _load_module(VALIDATOR, "workflow_contract_validator_for_return")
        validator.validate_handoff(template)
        manifest_bytes = json.dumps(template, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        manifest_tree = _tree_with_file(repo, routing, manifest_path, manifest_bytes)
        manifest = _commit(repo, manifest_tree, routing, args.manifest_message, args.commit_date)
        manifest_ref = f"{temp_prefix}/manifest"; _git(repo, "update-ref", manifest_ref, manifest); temp_refs.append(manifest_ref)
        _assert_manifest_only(repo, routing, manifest, manifest_path)
        manifest_report, manifest_digest = run_preflight(repo, routing, manifest, "manifest")
        reports = [("substantive", substantive_report, substantive_digest), ("manifest", manifest_report, manifest_digest)]
        _classification_template(classification, reports)

        branches = {args.result_branch: result, args.routing_branch: routing, args.manifest_branch: manifest}
        if args.push and not args.manual_review:
            raise Stop("push requires explicit completed manual review")
        if args.push and any(report["status"] != "CLEAN" for _, report, _ in reports):
            if not args.classifications:
                raise Stop(f"preflight findings require manual classification: {classification}")
            _validate_classifications(_outside(repo, args.classifications), reports)
        if _git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines() != status:
            raise Stop("worktree/index changed during preparation")
        _install_refs(repo, args.result_branch, result, base, args.routing_branch, routing,
                      args.manifest_branch, manifest)
        if _git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout.strip():
            raise Stop("result branch is not clean after atomic ref installation")
        if args.push:
            _push(repo, args.remote, branches)
        return {"base_sha": base, "result_sha": result, "routing_sha": routing,
                "manifest_sha": manifest, "classification_template": str(classification),
                "pushed": str(bool(args.push)).lower()}
    finally:
        for ref in reversed(temp_refs):
            _git(repo, "update-ref", "-d", ref, check=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    item = sub.add_parser("publish")
    item.add_argument("--repo-root", required=True)
    item.add_argument("--remote", default="origin")
    item.add_argument("--base", required=True)
    item.add_argument("--result-branch", required=True)
    item.add_argument("--routing-branch", required=True)
    item.add_argument("--manifest-branch", required=True)
    item.add_argument("--work-branch", required=True)
    item.add_argument("--handoff-source", required=True)
    item.add_argument("--handoff-path", required=True)
    item.add_argument("--manifest-template", required=True)
    item.add_argument("--manifest-path", required=True)
    item.add_argument("--classification-template", required=True)
    item.add_argument("--result-message", required=True)
    item.add_argument("--routing-message", required=True)
    item.add_argument("--manifest-message", required=True)
    item.add_argument("--commit-date", required=True)
    item.add_argument("--classifications")
    item.add_argument("--manual-review", action="store_true")
    item.add_argument("--push", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = publish(args)
    except (Stop, OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
