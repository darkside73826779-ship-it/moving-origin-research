#!/usr/bin/env python3
"""Create and remove exact-SHA, isolated MOR review worktrees."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SHA_RE = re.compile(r"[0-9a-f]{40}")
REF_RE = re.compile(r"refs/heads/[A-Za-z0-9._/-]+")
BRANCH_RE = re.compile(r"(?!-)(?!.*(?:^|/)\.\.?($|/))[A-Za-z0-9._/-]+")
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKER = b"moving-origin-research-workspace-v1\n"


class Stop(RuntimeError):
    """A fail-closed contract violation."""


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, encoding="utf-8", errors="strict",
    )
    if check and result.returncode:
        raise Stop(f"git command failed: {' '.join(args)}: {result.stderr.strip()}")
    return result


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _resolved_existing_dir(value: str, label: str) -> Path:
    supplied = Path(value)
    if not supplied.is_absolute() or not supplied.is_dir():
        raise Stop(f"{label} must be an absolute existing directory")
    return supplied.resolve(strict=True)


def _validate_sha(value: str, label: str) -> str:
    if not SHA_RE.fullmatch(value):
        raise Stop(f"{label} must be lowercase 40-hex")
    return value


def _is_strict_child(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return child != parent


def _worktrees(repo: Path) -> list[Path]:
    raw = _git(repo, "worktree", "list", "--porcelain", "-z").stdout
    result: list[Path] = []
    for record in raw.split("\0\0"):
        for field in record.split("\0"):
            if field.startswith("worktree "):
                result.append(Path(field[9:]).resolve(strict=False))
    return result


def _overlaps(candidate: Path, existing: Path) -> bool:
    return candidate == existing or _is_strict_child(candidate, existing) or _is_strict_child(existing, candidate)


def _clean(repo: Path) -> bool:
    return _git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout == ""


def _is_ancestor(repo: Path, old: str, new: str) -> bool:
    return _git(repo, "merge-base", "--is-ancestor", old, new, check=False).returncode == 0


def _receipt_payload(args: argparse.Namespace, repo: Path, root: Path, worktree: Path, created: str) -> dict[str, Any]:
    return {
        "base_sha": args.base,
        "created_utc": created,
        "remote_ref": args.ref,
        "repo_path": str(repo),
        "review_result_sha": None if args.review_result == "none" else args.review_result,
        "routing_ref_sha": args.ref_head,
        "work_branch": args.work_branch,
        "workspace_root": str(root),
        "worktree_path": str(worktree),
    }


def _write_receipt(root: Path, worktree: Path, payload: dict[str, Any]) -> Path:
    # The digest covers the complete payload before the digest member is attached.
    document = dict(payload)
    document["receipt_sha256"] = hashlib.sha256(_canonical(payload)).hexdigest()
    receipt = root / f".{worktree.name}.receipt.json"
    if receipt.exists():
        raise Stop("receipt path already exists")
    receipt.write_bytes(_canonical(document) + b"\n")
    return receipt


def create(args: argparse.Namespace) -> Path:
    repo = _resolved_existing_dir(args.repo, "repo")
    root = _resolved_existing_dir(args.workspace_root, "workspace-root")
    if (root / ".mor-workspace-root").read_bytes() != MARKER:
        raise Stop("workspace marker is missing or has incorrect bytes")
    _validate_sha(args.ref_head, "ref-head")
    _validate_sha(args.base, "base")
    review = None if args.review_result == "none" else _validate_sha(args.review_result, "review-result")
    if not REF_RE.fullmatch(args.ref) or ".." in args.ref.split("/"):
        raise Stop("ref must be a full refs/heads reference")
    if not BRANCH_RE.fullmatch(args.work_branch) or args.work_branch.endswith((".", "/")) or ".." in args.work_branch:
        raise Stop("invalid work branch")
    if not SLUG_RE.fullmatch(args.work_item):
        raise Stop("work-item must be a lowercase hyphenated slug")
    if _git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise Stop("repo is not a Git worktree")

    remote_rows = [row.split() for row in _git(repo, "ls-remote", "--refs", args.remote, args.ref).stdout.splitlines() if row.strip()]
    if len(remote_rows) != 1 or len(remote_rows[0]) != 2 or remote_rows[0] != [args.ref_head, args.ref]:
        raise Stop("remote ref is ambiguous or does not equal ref-head")
    private_ref = f"refs/mor/intake/{args.ref_head}"
    _git(repo, "fetch", "--no-tags", args.remote, f"{args.ref}:{private_ref}")
    if _git(repo, "rev-parse", "--verify", private_ref).stdout.strip() != args.ref_head:
        raise Stop("fetched private ref mismatch")
    _git(repo, "cat-file", "-e", f"{args.base}^{{commit}}")
    if review is not None:
        _git(repo, "cat-file", "-e", f"{review}^{{commit}}")
        if args.base != review and not _is_ancestor(repo, args.base, review):
            raise Stop("base is not review-result or its ancestor")
        if review != args.ref_head and not _is_ancestor(repo, review, args.ref_head):
            raise Stop("review-result is not ref-head or its ancestor")
        if review != args.ref_head:
            changed = _git(repo, "diff", "--name-only", "-z", review, args.ref_head).stdout.split("\0")
            if any(path and not path.startswith("handoffs/") for path in changed):
                raise Stop("routing-only range changes a non-handoffs path")
    elif args.base != args.ref_head and not _is_ancestor(repo, args.base, args.ref_head):
        raise Stop("base is not ref-head or its ancestor")

    if _git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{args.work_branch}", check=False).returncode == 0:
        raise Stop("local work branch already exists")
    remote_branch = _git(repo, "ls-remote", "--heads", args.remote, f"refs/heads/{args.work_branch}").stdout
    if remote_branch.strip():
        raise Stop("remote work branch already exists")

    worktree = (root / f"mor-{args.work_item}-{args.ref_head[:12]}").resolve(strict=False)
    if not _is_strict_child(worktree, root) or worktree.exists():
        raise Stop("worktree path is not a new strict child of workspace-root")
    if any(_overlaps(worktree, existing) for existing in _worktrees(repo)):
        raise Stop("worktree path overlaps an existing registered worktree")
    _git(repo, "worktree", "add", "--detach", str(worktree), args.ref_head)
    # A failure after worktree creation deliberately stops without cleanup guessing.
    if worktree.resolve(strict=True) != worktree or _git(worktree, "rev-parse", "HEAD").stdout.strip() != args.ref_head:
        raise Stop("created worktree identity mismatch")
    if review is not None:
        _git(worktree, "cat-file", "-e", f"{review}^{{commit}}")
    if not _clean(worktree):
        raise Stop("created worktree is dirty")
    _git(worktree, "switch", "-c", args.work_branch, args.ref_head)
    if _git(worktree, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != args.work_branch:
        raise Stop("declared work branch was not created")
    return _write_receipt(root, worktree, _receipt_payload(args, repo, root, worktree, datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")))


def _load_receipt(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            raise Stop("receipt is not canonical single-LF JSON")
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Stop(f"invalid receipt: {exc}") from exc
    required = {"base_sha", "created_utc", "remote_ref", "repo_path", "review_result_sha", "routing_ref_sha", "work_branch", "workspace_root", "worktree_path", "receipt_sha256"}
    if not isinstance(value, dict) or set(value) != required or raw != _canonical(value) + b"\n":
        raise Stop("receipt fields or canonical encoding are invalid")
    supplied = value.pop("receipt_sha256")
    if not isinstance(supplied, str) or supplied != hashlib.sha256(_canonical(value)).hexdigest():
        raise Stop("receipt digest mismatch")
    value["receipt_sha256"] = supplied
    return value


def cleanup(args: argparse.Namespace) -> None:
    receipt = Path(args.receipt)
    if not receipt.is_absolute() or not receipt.is_file():
        raise Stop("receipt must be an absolute existing file")
    receipt = receipt.resolve(strict=True)
    value = _load_receipt(receipt)
    repo = Path(value["repo_path"]).resolve(strict=True)
    root = Path(value["workspace_root"]).resolve(strict=True)
    worktree = Path(value["worktree_path"]).resolve(strict=True)
    if receipt.parent != root or (root / ".mor-workspace-root").read_bytes() != MARKER:
        raise Stop("receipt root or workspace marker mismatch")
    if not _is_strict_child(worktree, root):
        raise Stop("worktree is not a strict child of workspace-root")
    registered = _worktrees(repo)
    if registered.count(worktree) != 1:
        raise Stop("receipt worktree is not exactly registered")
    if any(other != worktree and _is_strict_child(other, worktree) for other in registered):
        raise Stop("registered nested worktree exists")
    if _git(worktree, "rev-parse", "HEAD").stdout.strip() != value["routing_ref_sha"]:
        raise Stop("worktree HEAD no longer equals routing-ref SHA")
    review = value["review_result_sha"]
    if review is not None and review != value["routing_ref_sha"] and not _is_ancestor(worktree, review, value["routing_ref_sha"]):
        raise Stop("review-result ancestry check failed")
    if not _clean(worktree):
        raise Stop("worktree is dirty")
    _git(repo, "worktree", "remove", str(worktree))
    receipt.unlink()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("create")
    for flag in ("repo", "remote", "ref", "ref-head", "review-result", "base", "work-branch", "workspace-root", "work-item"):
        make.add_argument(f"--{flag}", required=True)
    remove = commands.add_parser("cleanup")
    remove.add_argument("--receipt", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "create":
            print(create(args))
        else:
            cleanup(args)
        return 0
    except (Stop, OSError, UnicodeError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
