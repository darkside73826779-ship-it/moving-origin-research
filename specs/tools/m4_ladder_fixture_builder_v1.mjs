import fs from "node:fs";
import crypto from "node:crypto";

const root = "specs/data/";
const read = (name) => JSON.parse(fs.readFileSync(root + name));
const canonical = (value) => Array.isArray(value) ? `[${value.map(canonical).join(",")}]` : value !== null && typeof value === "object" ? `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}` : JSON.stringify(value);
const write = (name, value) => {
  fs.writeFileSync(root + name, canonical(value) + "\n");
  const digest = crypto.createHash("sha256").update(fs.readFileSync(root + name)).digest("hex");
  fs.writeFileSync(root + name + ".sha256", `${digest}  ${name}\n`);
};

const ids = ["STACK_INDEX", "STACK_PLATFORM", "CHECKPOINT_FILES", "CANDIDATE_PEER_EQUALITY", "FP8_METADATA", "FP8_FINITE_LOGITS", "FORMAT_JSON", "CONTEXT_1024", "CONTEXT_4096", "CONTEXT_8192"];
const schema = read("m4_model_preflight_result_schema_v1.json");
delete schema.properties.fp8_checks;
delete schema.properties.context_checks;
schema.properties.checks = { type: "array", items: { $ref: "#/$defs/check" }, maxItems: 10 };
schema.required = schema.required.map((x) => x === "fp8_checks" ? "checks" : x).filter((x) => x !== "context_checks");
schema.allOf = [{
  if: { properties: { status: { const: "PASS" } }, required: ["status"] },
  then: { properties: { checks: { minItems: 10, maxItems: 10, prefixItems: ids.map((id, ordinal) => ({ properties: { ordinal: { const: ordinal }, check_id: { const: id }, status: { const: "PASS" } }, required: ["ordinal", "check_id", "status"] })) } } },
}];
write("m4_model_preflight_result_schema_v1.json", schema);

for (const name of ["m4_model_preflight_result_blocked_v1.json", "m4_model_preflight_result_fail_v1.json"]) {
  const value = read(name);
  delete value.fp8_checks;
  delete value.context_checks;
  value.checks = [];
  write(name, value);
}

const pass = read("m4_model_preflight_result_pass_v1.json");
delete pass.fp8_checks;
delete pass.context_checks;
const rows = [
  ["STACK_INDEX", "sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db", "sha256:607442e407b0fea97f8a132a78b787c121a996dd4de181fa08e8da06e71ec2db"],
  ["STACK_PLATFORM", "sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6", "sha256:df2607b26bdda2875de4832f4d08da0055b4b6e3570347f3a849bcc652771dd6"],
  ["CHECKPOINT_FILES", true, true], ["CANDIDATE_PEER_EQUALITY", true, true], ["FP8_METADATA", "E4M3", "E4M3"], ["FP8_FINITE_LOGITS", true, true],
  ["FORMAT_JSON", "{\"answer\":\"A\"}", "{\"answer\":\"A\"}"], ["CONTEXT_1024", 1024, 1024], ["CONTEXT_4096", 4096, 4096], ["CONTEXT_8192", 8192, 8192],
];
pass.checks = rows.map(([check_id, expected, observed], ordinal) => ({ check_id, expected, observed, ordinal, status: "PASS" }));
write("m4_model_preflight_result_pass_v1.json", pass);

const transcript = read("m4_phase_a_transcript_valid_v1.json");
transcript.peer_projection_sha256 = "49bbf38b93bafdaeb6f7e8e38712d88686f15f9ab98034d95c1678036f989c51";
write("m4_phase_a_transcript_valid_v1.json", transcript);
