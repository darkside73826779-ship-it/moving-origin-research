# M3/E2 V4.4 Implementation Record
- Retained all prior L3 failures at ec457fc/6ef3cce/76a8dd6 and L1 seed-102 false failure.
- Added frozen SHA-256-CTR/Fisher-Yates/Box-Muller RNG and exact subdraw custody.
- Applied 1,000-draw, ties-adverse plus-one family tests to the nine stochastic controls.
- Implemented L1 one-sided null-of-max shuffle and retained all deterministic L1 checks.
- Implemented amended L3 burn-in, delay state, paired shuffle control, and raw evidence.
- Restored and gated every exact L5 control; candidate access-count mismatch remains KILL.
- Added content-addressed raw draw manifests with fail-closed schema/RNG validation.
- Retained seeds 201–203 are rejected; no scoring, hold-out execution, or courier occurred.
- Dev 101–105 first pass was all PASS; post-fix L5 verification is separately preserved.
