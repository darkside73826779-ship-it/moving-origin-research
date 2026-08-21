import fs from "node:fs";
import crypto from "node:crypto";

const fixture = JSON.parse(fs.readFileSync("specs/data/m4_model_callable_fixture_v1.json"));
const base = JSON.parse(fs.readFileSync("specs/data/m4_model_scaffold_executable_fixture_v1.json"));
const canonical = (v) => Array.isArray(v) ? `[${v.map(canonical).join(",")}]` : v !== null && typeof v === "object" ? `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canonical(v[k])}`).join(",")}}` : JSON.stringify(v);
const bytes = (v) => Buffer.from(canonical(v));
const sha = (v) => crypto.createHash("sha256").update(bytes(v)).digest("hex");
const wrap = (artifact) => ({ artifact, canonical_utf8_base64: bytes(artifact).toString("base64"), expected_sha256: sha(artifact) });

const ready = fixture.lifecycle_state_contract.states.ready.artifact;
const readySha = sha(ready);
const steppedBasis = structuredClone(fixture.lifecycle_state_contract.states.stepped.artifact);
steppedBasis.episode_id = fixture.varying_candidate.request_patch[0][1];
steppedBasis.last_response_sha256 = null;
const steppedProjection = structuredClone(steppedBasis);
delete steppedProjection.last_response_sha256;
const steppedProjectionSha = sha(steppedProjection);

const common = structuredClone(base.response_constructor.common);
common.episode_id = "callable-episode-0";
common.state_before_sha256 = readySha;
common.state_after_sha256 = steppedProjectionSha;
common.resource_report.dependency_manifest_sha256 = fixture.dependency_manifest.expected_sha256;
const response = { ...common, role: "candidate", scientific_arm: "candidate", ...fixture.varying_candidate.expected_output };
const responseSha = sha(response);

const stepped = structuredClone(steppedBasis);
stepped.last_response_sha256 = responseSha;
const steppedSha = sha(stepped);

const operation = structuredClone(fixture.lifecycle_state_contract.operation_results.step.artifact);
operation.prior_state_sha256 = readySha;
operation.post_state_sha256 = steppedSha;

const snapshotRequest = structuredClone(fixture.snapshot_fixture.request);
snapshotRequest.expected_state_sha256 = steppedSha;

const snapshotted = structuredClone(fixture.lifecycle_state_contract.states.snapshotted.artifact);
snapshotted.last_response_sha256 = responseSha;
const snapshottedSha = sha(snapshotted);
const snapshotOperation = structuredClone(fixture.lifecycle_state_contract.operation_results.snapshot.artifact);
snapshotOperation.prior_state_sha256 = steppedSha;
snapshotOperation.post_state_sha256 = snapshottedSha;

const closed = structuredClone(fixture.lifecycle_state_contract.states.closed.artifact);
closed.last_response_sha256 = responseSha;
const closedSha = sha(closed);
const closeOperation = structuredClone(fixture.lifecycle_state_contract.operation_results.close.artifact);
closeOperation.prior_state_sha256 = snapshottedSha;
closeOperation.post_state_sha256 = closedSha;

const amendment = {
  schema_version: "m4-callable-step-digest-amendment-v1",
  date: "2026-08-21",
  regime: "B",
  source_class: "PROPOSED",
  base: { commit: "ade99fc13dc750b789d254316b9a7dc5de2eae8b", path: "specs/data/m4_model_callable_fixture_v1.json", raw_sha256: crypto.createHash("sha256").update(fs.readFileSync("specs/data/m4_model_callable_fixture_v1.json")).digest("hex") },
  precedence: "These wrappers replace only varying_candidate.expected_response_sha256, lifecycle_state_contract.states.stepped/snapshotted/closed, lifecycle_state_contract.operation_results.step/snapshot/close, and snapshot_fixture request/digest. All other base bytes remain operative.",
  digest_domains: {
    complete_state: "SHA-256 RFC-8785 complete state bytes without LF",
    post_state_projection: "SHA-256 RFC-8785 bytes without LF after deleting exactly /last_response_sha256 from the constructed post-state",
    response: "SHA-256 RFC-8785 complete response bytes without LF",
    operation_result: "SHA-256 RFC-8785 complete operation-result bytes without LF"
  },
  construction_order: ["validate request correlation", "hash complete pre-state", "construct post-state with last_response_sha256=null", "delete /last_response_sha256 and hash post-state projection", "construct response using pre-state digest and post-state-projection digest", "hash complete response", "insert response digest into complete post-state", "hash complete post-state", "construct and hash operation result"],
  response_state_after_semantics: "state_after_sha256 is the post-state-projection digest, not the complete post-state digest; operation_result.post_state_sha256 is the complete post-state digest",
  varying_response: wrap(response),
  stepped_state_projection: wrap(steppedProjection),
  stepped_state: wrap(stepped),
  step_operation_result: wrap(operation),
  snapshot_request: wrap(snapshotRequest),
  snapshotted_state: wrap(snapshotted),
  snapshot_operation_result: wrap(snapshotOperation),
  closed_state: wrap(closed),
  close_operation_result: wrap(closeOperation),
  invariants: { response_episode_equals_request_episode: response.episode_id === "callable-episode-0", response_state_before_equals_complete_pre_state: response.state_before_sha256 === readySha, response_state_after_equals_projection: response.state_after_sha256 === steppedProjectionSha, complete_post_state_records_response: stepped.last_response_sha256 === responseSha, no_digest_cycle: true }
};

fs.writeFileSync("specs/data/m4_callable_step_digest_amendment_v1.json", canonical(amendment) + "\n");
const raw = crypto.createHash("sha256").update(fs.readFileSync("specs/data/m4_callable_step_digest_amendment_v1.json")).digest("hex");
fs.writeFileSync("specs/data/m4_callable_step_digest_amendment_v1.json.sha256", `${raw}  m4_callable_step_digest_amendment_v1.json\n`);
