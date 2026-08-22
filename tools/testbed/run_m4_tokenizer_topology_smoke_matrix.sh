#!/usr/bin/env bash
set -euo pipefail

repo="$1"
image="docker.io/vllm/vllm-openai@sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6"
failure="RUNTIME_IDENTITY_MISMATCH_NO_CUSTODY_NO_CONSUMPTION_STOP_NO_RETRY"
empty_sha="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
root="$(mktemp -d)"
cleanup() {
  rm -rf -- "$root"
}
trap cleanup EXIT

unset MOR_CUSTODY_M4_QWEN3_4B_FP8_PRESERVED_V1
test -f "$repo/artifacts/m4_tokenizer_materialization/.gitkeep"
test ! -L "$repo/artifacts/m4_tokenizer_materialization/.gitkeep"
test ! -s "$repo/artifacts/m4_tokenizer_materialization/.gitkeep"

run_positive() {
  local stage="$root/positive-stage"
  mkdir -m 700 "$stage"
  docker run --rm --pull=never --platform linux/amd64 --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --mount "type=bind,src=$repo,dst=/workspace,readonly" \
    --mount "type=bind,src=$stage,dst=/workspace/artifacts/m4_tokenizer_materialization" \
    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 \
    --workdir /workspace --entrypoint /bin/true "$image"
  test -z "$(find "$stage" -mindepth 1 -print -quit)"
  printf 'test_mount_smoke_positive_repository_then_nested_output exit=0 stage=empty mapping=PROCEED_TO_SINGLE_MATERIALIZATION_RELEASE_CHECK\n'
}

run_absent_marker() {
  local snapshot="$root/absent-marker-checkout"
  local stage="$root/absent-marker-stage"
  local error="$root/absent-marker-engine.stderr"
  mkdir -m 700 "$snapshot" "$stage"
  tar -C "$repo" --exclude=.git -cf - . | tar -C "$snapshot" -xf -
  rm -f -- "$snapshot/artifacts/m4_tokenizer_materialization/.gitkeep"
  rmdir -- "$snapshot/artifacts/m4_tokenizer_materialization"
  set +e
  docker run --rm --pull=never --platform linux/amd64 --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --mount "type=bind,src=$snapshot,dst=/workspace,readonly" \
    --mount "type=bind,src=$stage,dst=/workspace/artifacts/m4_tokenizer_materialization" \
    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 \
    --workdir /workspace --entrypoint /bin/true "$image" >/dev/null 2>"$error"
  local exit_code=$?
  set -e
  test "$exit_code" -eq 125
  test -z "$(find "$stage" -mindepth 1 -print -quit)"
  printf 'mount_smoke_negative_absent_marker_engine_125 exit=125 stage=empty mapping=%s\n' "$failure"
}

run_reversed_mounts() {
  local stage="$root/reversed-stage"
  local error="$root/reversed-engine.stderr"
  mkdir -m 700 "$stage"
  set +e
  docker run --rm --pull=never --platform linux/amd64 --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --mount "type=bind,src=$stage,dst=/workspace/artifacts/m4_tokenizer_materialization" \
    --mount "type=bind,src=$repo,dst=/workspace,readonly" \
    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 \
    --workdir /workspace --entrypoint /bin/true "$image" >/dev/null 2>"$error"
  local exit_code=$?
  set -e
  test -z "$(find "$stage" -mindepth 1 -print -quit)"
  printf 'test_mount_smoke_negative_nested_output_before_repository exit=%s stage=empty mapping=%s\n' "$exit_code" "$failure"
}

run_nonempty_postcondition() {
  local stage="$root/nonempty-stage"
  local sentinel="$stage/unexpected-after-smoke.txt"
  mkdir -m 700 "$stage"
  docker run --rm --pull=never --platform linux/amd64 --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --mount "type=bind,src=$repo,dst=/workspace,readonly" \
    --mount "type=bind,src=$stage,dst=/workspace/artifacts/m4_tokenizer_materialization" \
    --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m,mode=0700 \
    --workdir /workspace --entrypoint /bin/true "$image"
  : >"$sentinel"
  test "$(find "$stage" -mindepth 1 -maxdepth 1 -printf '%f\n')" = "unexpected-after-smoke.txt"
  test "$(sha256sum "$sentinel" | cut -d' ' -f1)" = "$empty_sha"
  rm -f -- "$sentinel"
  test -z "$(find "$stage" -mindepth 1 -print -quit)"
  printf 'test_mount_smoke_negative_nonempty_stage_after_smoke exit=0 observed_stage=unexpected-after-smoke.txt cleanup=empty mapping=%s\n' "$failure"
}

run_positive
run_absent_marker
run_reversed_mounts
run_nonempty_postcondition
printf 'TOPOLOGY_SMOKE_MATRIX_PASS custody_environment=false custody_mount=false custody_record=false model_tokenizer_access=false materializer_started=false operation_consumed=false retry=false cleanup=complete\n'
