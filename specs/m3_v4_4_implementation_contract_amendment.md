# M3 V4.4 Implementation-Completeness Amendment

**Status:** DRAFT FOR INDEPENDENT CRITIC REVIEW — no implementation or scoring authorization

**Date:** 2026-08-16

**Author:** ARCHITECT

**Gate served:** M3 V4.4 Implementation-Completeness Amendment Gate (per WORKFLOW COORDINATOR routing, 2026-08-16 19:24 EDT)

**Authoritative base:** `45736cb` (GitHub main)

**Scope:** This companion document defines seven implementation-level contracts that V4.4 left unspecified. It does NOT revise the V4.4 specification's bars, control transforms, verdict semantics, seed pools, authorization boundaries, or candidate-facing conditions. It completes implementation-level detail within the already-approved V4.4 structure. The three CRITIC-cleared L1 V4.4 amendments (one-sided directionality, null-of-the-max, §2.10 harmonization) are NOT reopened. No implementation, code execution, scoring, or seed exposure occurred.

---

## Contract 1 — Gaussian generation from SHA-256 stream (resolves PRIMARY BLOCK)

V4.4 §6 defines uniform integers, Fisher–Yates permutations, and derangements from the SHA-256 counter-mode stream but does not define the transformation from stream words to Gaussian values required by the L3 AR(3) innovation draws `ε[t] ~ N(0, σ²)` with `σ² = 0.05`.

### 1.1 Method: Box–Muller transform

The Gaussian generation method is **Box–Muller** using two 53-bit mantissa uniforms from the SHA-256 stream.

### 1.2 Uniform extraction

From each 64-bit big-endian stream word `w`:
1. Extract the low 53 bits: `m = w & ((1 << 53) - 1)`.
2. Convert to open-interval uniform: `u = m / 2^53`. This yields `u ∈ [0, 1)`.

### 1.3 Pair consumption and Gaussian computation (B3 fix — cursor-level pseudocode)

The stream is consumed via a monotonically advancing cursor. Each call to `next_word()` reads `stream_word[cursor]` and increments `cursor` by 1. The Gaussian generation loop is:

```
cursor = 0
rejection_count = 0

next_word():
  w = stream_word[cursor]
  cursor += 1
  return w

next_open_u1():
  while true:
    w1 = next_word()
    m1 = low53(w1)
    if m1 != 0:
      return m1 / 2^53
    rejection_count += 1

next_gaussian_pair():
  u1 = next_open_u1()      // consumes ≥1 word; rejected words advance cursor by 1 each
  w2 = next_word()           // consumes exactly 1 word
  u2 = low53(w2) / 2^53     // u2=0 is valid; no adjustment, no rejection
  r = sqrt(-2 * ln(u1))
  theta = 2 * π * u2
  return (r * cos(theta), r * sin(theta))
```

Key properties:
- `u1` consumption: read words one at a time until `low53(w) != 0`. Each rejected word advances the cursor by exactly 1.
- `u2` consumption: read exactly 1 word. `u2 = 0` is valid (produces `theta = 0`, `cos = 1`, `sin = 0`). No special case, no adjustment.
- The next Gaussian pair begins at the cursor position immediately after the `u2` word. No word skipping, no partner promotion.
- Both `z1 = r * cos(theta)` and `z2 = r * sin(theta)` are standard normal `N(0, 1)` values. They are emitted as a pair: `z1` first, then `z2`.

**Forced rejection conformance case (B3 fix):**

To eliminate any residual ambiguity, the following synthetic case shows exact cursor behavior when a rejection occurs:

```
word[0] low53 = 0  → rejected as u1 candidate; cursor=1; rejection_count=1
word[1] low53 = 1  → accepted; u1 = 2^-53; cursor=2
word[2] low53 = 2^52 → u2 = 0.5; cursor=3
// Gaussian pair: z1 = sqrt(-2*ln(2^-53)) * cos(π), z2 = sqrt(-2*ln(2^-53)) * sin(π)
// Next pair begins reading at word[3]
```

This rules out Interpretation A (partner-skipping) and Interpretation C (word promotion). Only Interpretation B (sequential cursor) is correct.

### 1.4 Scaling

Scale to the L3 innovation distribution: `ε = sqrt(0.05) * z`, where `0.05` is the variance and `sqrt(0.05) ≈ 0.22360679774997896` (binary64, rounded once).

### 1.5 Array fill order

Gaussian values fill the innovation array in **channel-major, time-major** order: `ε[t_abs, c]` for `t_abs = 0..1109` (including burn-in), `c = 0..7`. The Box–Muller pair `(z1, z2)` fills consecutive array positions: `ε[t_abs, c] = sqrt(0.05) * z1`, `ε[t_abs, c+1] = sqrt(0.05) * z2` (if `c+1 < 8`), or `ε[t_abs, c+1] = sqrt(0.05) * z1_next` if the channel wraps. Specifically: the flat index `i = t_abs * 8 + c` maps to Box–Muller pair `i // 2`, component `i % 2` (0 = cos/z1, 1 = sin/z2).

Since `8` is even, each time step's 8 channels consume exactly 4 Box–Muller pairs (8 stream words). The full sequence (1110 time steps × 8 channels = 8880 values) consumes exactly 4440 pairs = **8880 stream words** (assuming zero rejections).

### 1.6 Rejection accounting

The rejection counter tracks the total number of rejected `w1` words (where `low53(w1) == 0`). The expected rejection count is 8880 / 2^53 ≈ 0. The rejection count is included in the RNG artifact record.

### 1.7 Conformance vectors (B1 fix — tolerance-based, not bit-exact; NB1 — implementation-emitted)

For cross-platform verification, the **implementation emits** the following conformance vectors in the RNG artifact record. JUDGE independently recomputes them: `u1`/`u2` mantissa values must reproduce **bit-exactly** (under C6.5, integer arithmetic); `z1`, `z2`, and scaled `ε` values must reproduce **within the C6.2 transcendental tolerance** (1e-12 relative, 1e-14 absolute for near-zero).

- **Vector A (first 10 pairs):** the first 20 consumed stream words (including any rejected words), their 53-bit mantissas, the resulting `u1, u2, z1, z2`, and the scaled `ε` values. JUDGE recomputes `u1`/`u2` bit-exactly and `z`/`ε` within tolerance.
- **Vector B (full-sequence digest):** SHA-256 of the complete 8880-value `ε` array in C-row-major little-endian binary64. This digest is an **artifact-custody digest** — it verifies that the implementation's stored array matches its own output. It is NOT a cross-platform pass/fail reference: JUDGE recomputes the `ε` array from the stream and tolerance-checks element-wise, not by digest equality across platforms.

---

## Contract 2 — AR(3) initialization (resolves gap 2)

### 2.1 Initial conditions

The AR(3) recursion `x[t] = a1·x[t-1] + a2·x[t-2] + a3·x[t-3] + sin_term + ε[t]` requires initial values for `x[-3], x[-2], x[-1]`. These are **fixed zeros**: `x[-3] = x[-2] = x[-1] = 0` (all 8 channels).

### 2.2 Burn-in specification (B2 fix — corrected timeline)

- **Burn-in length:** 100 cycles, generated before the scored sequence.
- **Generation timeline (corrected):** the AR(3) recursion runs for `t_abs = 0..1109` (**1110 total cycles** generated, including burn-in). The first 100 cycles (`t_abs = 0..99`) are the **burn-in** and are discarded. The scored sequence is `t_abs = 100..1109` (**1010 cycles**), re-indexed as `t = 0..1009` in the scored output.
- **Sinusoid time index:** the sinusoid uses **absolute pre-burn-in time**: `sin_term = 0.5 * sin(2π·t_abs / 7 + phase_c)` where `t_abs` is the absolute index from the start of generation (0-based). The scored sequence's `t = 0` corresponds to `t_abs = 100`.
- **Innovation consumption:** innovations are generated for all 1110 cycles (`ε[t_abs, c]` for `t_abs = 0..1109`, `c = 0..7`, total 8880 values). Burn-in innovations are consumed from the RNG stream but their resulting sequence values are discarded.
- **Consistency check:** evaluation origin at scored `t = 904` (absolute `t_abs = 1004`) with horizon 5 reaches scored `t = 909` (absolute `t_abs = 1109`), which is the last generated cycle — exactly matching the 1010-cycle scored sequence length and the 1110-cycle total generation.

### 2.3 Channel ordering

Channels are indexed `c = 0..7` in a fixed order. The innovation array `ε[t_abs, c]` is filled in channel-major, time-major order (Contract 1.5).

---

## Contract 3 — Subdraw registry (resolves gap 3)

Each stochastic family may require multiple stochastic components per draw. The `subdraw_index` in the RNG key (§6) identifies which component a given stream produces. The complete registry:

### 3.1 L1 families

| Family | Role | Subdraw | Component | Type | Size |
|---|---|---|---|---|---|
| L1.frozen | OBSERVED, NULL | 0 | Tie-break reassignment permutation | Fisher–Yates | 200 elements |
| L1.fair_naive | OBSERVED, NULL | 0 | Identifier permutation | Fisher–Yates | 200 elements |
| L1.permuted | OBSERVED, NULL | 0 | (age,rehearsal)→entry mapping permutation | Fisher–Yates | 200 elements |
| L1.shuffled | OBSERVED, NULL | 0 | Priming query reassignment | Fisher–Yates | 1200 elements |

All L1 stochastic families use a single subdraw (index 0). The observed draw and each null replicate use the same subdraw_index.

### 3.2 L3 families

| Family | Role | Subdraw | Component | Type | Size |
|---|---|---|---|---|---|
| L3.frozen | OBSERVED, NULL | 0 | Gaussian innovations | Box–Muller | 8880 values (1110×8) |
| L3.oracle | OBSERVED, NULL | 0 | Gaussian innovations | Box–Muller | 8880 values (1110×8) |
| L3.permuted | OBSERVED | 0 | Gaussian innovations | Box–Muller | 8880 values (1110×8) |
| L3.permuted | OBSERVED | 1 | Channel derangement | Derangement (FY + reject) | 8 elements |
| L3.permuted | NULL | 0 | Channel derangement | Derangement (FY + reject) | 8 elements |
| L3.shuffled | OBSERVED | 0 | Gaussian innovations | Box–Muller | 8880 values (1110×8) |
| L3.shuffled | OBSERVED | 1 | Cycle-order permutation | Fisher–Yates | 1010 elements |
| L3.shuffled | NULL | 0 | Cycle-order permutation | Fisher–Yates | 1010 elements |

**Key distinction:** for L3.permuted and L3.shuffled, the NULL draws reuse the OBSERVED draw's sequence (innovations are not regenerated). The null RNG stream only generates the perturbation component (derangement or cycle-order permutation). The observed draw uses subdraw 0 for innovations and subdraw 1 for the perturbation. The null draws use subdraw 0 for the perturbation only.

For L3.frozen and L3.oracle, both observed and null draws generate fresh innovations (full pipeline rerun).

### 3.3 L5 families

| Family | Role | Subdraw | Component | Type | Size |
|---|---|---|---|---|---|
| L5.permuted | OBSERVED, NULL | 0 | Field derangement (acquired_at/validity) | Derangement (FY + reject) | 200 elements |
| L5.permuted | OBSERVED, NULL | 1 | Chain content derangement | Derangement (FY + reject) | 200 elements |

### 3.4 Uniqueness

Every `(law, arm, role, seed, replicate, subdraw)` tuple is consumed once only. Reuse is an INSTRUMENT FAILURE. The registry above defines the complete set of valid subdraw_index values for each family/role combination.

---

## Contract 4 — RNG artifact schema gaps (resolves gap 4)

### 4.1 Common RNG record (all families)

Every RNG derivation record contains:
```
{
  law: str,
  arm: str,
  draw_role: "OBSERVED" | "NULL",
  scoring_seed: int,
  replicate_index: int,
  subdraw_index: int,
  stream_key_hex: str,           // SHA-256 key hex
  stream_block_count: int,       // number of SHA-256 blocks consumed
  stream_word_count: int,        // number of 64-bit words consumed
  rejection_count: int,          // number of rejected uniform draws
  accepted_permutation: ... | null,  // family-specific (see below)
  sha256_digest: str             // SHA-256 of all consumed raw bytes
}
```

### 4.2 Family-specific `accepted_permutation` semantics

| Family/Role/Subdraw | `accepted_permutation` field | Type |
|---|---|---|
| L1.frozen (subdraw 0) | The accepted 200-element tie-break permutation | `int[200]` |
| L1.fair_naive (subdraw 0) | The accepted 200-element identifier permutation | `int[200]` |
| L1.permuted (subdraw 0) | The accepted 200-element mapping permutation | `int[200]` |
| L1.shuffled (subdraw 0) | The accepted 1200-element priming query permutation | `int[1200]` |
| L3.frozen (subdraw 0) | `null` — no permutation; this subdraw produces Gaussian innovations only | `null` |
| L3.oracle (subdraw 0) | `null` — no permutation; Gaussian innovations only | `null` |
| L3.permuted OBSERVED (subdraw 0) | `null` — Gaussian innovations only | `null` |
| L3.permuted (subdraw 1 OBSERVED / subdraw 0 NULL) | The accepted 8-element channel derangement | `int[8]` |
| L3.shuffled OBSERVED (subdraw 0) | `null` — Gaussian innovations only | `null` |
| L3.shuffled (subdraw 1 OBSERVED / subdraw 0 NULL) | The accepted 1010-element cycle-order permutation | `int[1010]` |
| L5.permuted (subdraw 0) | The accepted 200-element field derangement | `int[200]` |
| L5.permuted (subdraw 1) | The accepted 200-element chain content derangement | `int[200]` |

`accepted_permutation: null` is explicitly authorized for Gaussian-innovation-only subdraws. The `rejection_count` field for these subdraws counts Box–Muller `u1=0` rejections (expected 0). For permutation/derangement subdraws, it counts uniform-integer rejection-sampler rejections.

---

## Contract 5 — Validation-index naming (resolves gap 5)

V4.4 §6.1 uses "train/validation/evaluation indices" but the L3 mechanism (§3.4 of earlier spec versions) uses "fitting/buffer/evaluation." The frozen field names are:

### 5.1 Frozen index field names

| Field name | Description | Values |
|---|---|---|
| `fitting_origin_indices` | Fitting-window origin time indices | `int[700]` = {0, 1, ..., 699} |
| `buffer_cycle_indices` | Buffer cycles (fitting targets only, excluded from both origin sets) | `int[5]` = {700, 701, 702, 703, 704} |
| `evaluation_origin_indices` | Evaluation-window origin time indices | `int[300]` = {705, 706, ..., 1004} |
| `fit_target_indices_by_horizon` | Per-horizon fitting target ranges | `int[5][700]` |
| `evaluation_target_indices_by_horizon` | Per-horizon evaluation target ranges | `int[5][300]` |

### 5.2 Binding

These field names are binding in all raw artifact schemas, RNG records, and JUDGE recomputation contracts. The terms "train" and "validation" do not appear in any L3 artifact field name. The term "evaluation" is retained as it matches the mechanism.

---

## Contract 6 — Cross-platform numerical contract (resolves gap 6)

### 6.1 Floating-point format

All real-valued arrays are IEEE 754 binary64 (double precision). Every value must be finite (no NaN, no infinity); a non-finite value in any computed array is an INSTRUMENT FAILURE.

### 6.2 Transcendental evaluation (B1 fix — broadened from trigonometric to include ln and sqrt)

The `sin`, `cos`, `ln`, and `sqrt` functions are evaluated using the platform's standard C library `libm` implementation (or language-equivalent, e.g., Python `math` module). Cross-platform differences in the last ULP are expected for all transcendental functions. **Tolerance:** for all transcendental-dependent arrays (Gaussian innovations `ε`, predictions, losses, reductions, statistics), the JUDGE recomputation tolerance is `1e-12` relative error per element, or `1e-14` absolute error for near-zero values. Exact bit-equality is NOT required for transcendental-dependent quantities. The `u1`/`u2` mantissa values (integer arithmetic, C6.5) remain bit-exact; only the transcendental outputs (`z1`, `z2`, `ε`, and downstream arrays) are tolerance-checked.

### 6.3 OLS solver

The OLS fit uses `numpy.linalg.lstsq` with `rcond=None` (the harness's existing implementation). The JUDGE recomputation uses the same solver. Cross-platform differences in SVD-based least-squares solutions are expected. **Tolerance:** fitted weights must agree to `1e-10` relative error. Resulting predictions, losses, and reductions must agree to `1e-8` relative error.

### 6.4 Accumulation order

Summation is performed in the natural left-to-right order over the flattened array (NumPy default `np.sum`). The JUDGE recomputation uses the same order. No pairwise summation, no Kahan summation, no parallel reduction. Cross-platform differences from floating-point associativity are bounded by the tolerances in §6.2–6.3.

### 6.5 SHA-256 and integer arithmetic

SHA-256 hashing, 64-bit integer arithmetic, and rejection sampling are exact across platforms (no tolerance). The RNG stream, permutation indices, derangement indices, and rejection counts must be **bit-identical** across platforms.

### 6.6 Comparison tolerances for verdicts

- **Exact predicates** (deterministic families): bit-identical comparison. No tolerance.
- **Stochastic p-values:** the plus-one p-value `p_s = (1 + count) / 1001` is exact integer arithmetic. No tolerance.
- **Reduction/statistic comparisons within a p-value computation:** the observed and null statistics must agree to `1e-8` relative error between implementation and JUDGE. The rank/tie count is then computed on the JUDGE's recomputed values.
- **FWFP bounds:** exact integer arithmetic (`48/1001`). No tolerance.

### 6.7 Binary array encoding

Numeric arrays in artifacts use raw C-row-major little-endian:
- `int64` for indices and counts
- `binary64` (float64) for real values
- `uint8` restricted to {0, 1} for booleans

No padding, no compression. SHA-256 digests cover the raw byte content.

---

## Contract 7 — L3 lineage reconciliation (resolves gap 7)

### 7.1 The conflict

V4.4 §3 states "The V4.1 candidate definition and candidate-facing reduction bars remain unchanged." However, `src/m3_harness.py` at authoritative main (`45736cb`) implements the L3 Repair Proposal (`src/m3_L3_REPAIR_PROPOSAL.md`), which changed two L3 components from the V4.1 text:

1. **Generator:** V4.1 had a shared sinusoid `0.5·sin(2π·t/7)`. The repair introduced channel-specific phases: `0.5·sin(2π·t/7 + c·π/16)` for channel `c = 0..7`.
2. **State update:** V4.1 had `A_i = [[0.9, 0.1], [0.0, 0.5]]` (dead-coordinate filter). The repair introduced a two-slot delay state: `A_i = [[0, 0], [1, 0]]`, `B[2i, i] = 1`, storing `[x_i[t], x_i[t-1]]` per channel block.

The repair was necessary because the V4.1 shared sinusoid caused permuted-control failures (all permuted reductions > 0 on development seeds) and the V4.1 dead-coordinate state caused candidate failures (candidate reductions < 5% on development seeds). The repair was validated on development seeds 101–105 (see `src/m3_L3_REPAIR_PROPOSAL.md` five-seed validation table).

### 7.2 Binding ruling

**The L3 Repair Proposal (`src/m3_L3_REPAIR_PROPOSAL.md`), as implemented in `src/m3_harness.py` at commit `45736cb`, is the governing L3 generator and state definition for V4.4.** This supersedes the V4.1 generator and state text. Specifically:

- **Governing generator:** `x[t] = 0.3·x[t-1] − 0.2·x[t-2] + 0.1·x[t-3] + 0.5·sin(2π·t/7 + c·π/16) + ε[t]`, `ε[t] ~ N(0, 0.05)` (variance), 8 channels with channel-specific phases `phase_c = c·π/16`, 100-cycle burn-in from zeros.
- **Governing state:** `s[t] ∈ R^16`, per-channel block `[x_i[t], x_i[t-1]]`, update `A_i = [[0, 0], [1, 0]]`, `B[2i, i] = 1`, zero learned parameters, `s[0] = 0`.
- **Governing shuffled comparator:** frozen reduction computed on the same shuffled sequence used by the shuffled state and raw comparator (not the original unshuffled sequence).

### 7.3 What remains unchanged

The V4.1 **candidate-facing reduction bars** (≥5% at every horizon 1..5) remain unchanged. The V4.1 fitting/evaluation windows (§3.4), loss function (§3.6), and predictor class structure (§3.3) remain unchanged. The L3 control arm transforms (§3.1–§3.4 of V4.4) remain unchanged — only the underlying generator and state that produce the sequences and predictions are the repaired versions.

### 7.4 Preserved failures

The three preserved L3 failures (`ec457fc`, `6ef3cce`, `76a8dd6`) remain retained under their original labels. The repair proposal's development-phase study (seeds 101–105 only) is disclosed as pre-scoring diagnostic evidence, not as scoring evidence.

### 7.5 L3 oracle v_h score edge case (NB3 clarification)

V4.4 §3.2 defines `v_h = max(0.05 - oracle_reduction_h, oracle_reduction_h - 0.95)` and `S = max_h v_h`. When all oracle reductions are strictly inside `(0.05, 0.95)`, every `v_h < 0`, so `S < 0`. When any reduction equals exactly 0.05 or 0.95, the corresponding `v_h = 0`, so `S >= 0`. The upper-tail plus-one p-value test on `S` is mathematically correct in both cases: `S < 0` yields a large p-value (pass), and `S = 0` or `S > 0` is tested against the null distribution. JUDGE should document this explicitly: `v_h <= 0` for all horizons means the oracle is within both anchors and the family passes with a large p-value.

---

## No-change audit

- No candidate-facing bar changed (L1 R² ≥ 0.85, β_age < 0, ρ ≥ 0.6; L3 ≥ 5% reduction; L5 ≥ 0.95 accuracy, = 1.00 chain-walk; L6 8/4/6).
- No change that benefits the candidate (four-part test condition (b) stands).
- The three L1 V4.4 amendments (one-sided directionality, null-of-the-max, §2.10 harmonization) are NOT reopened.
- No seed pool, hold-out rule, verdict rule, authorization boundary, or INSTRUMENT_FAILURE handling changed.
- No implementation, code execution, scoring, or seed exposure occurred.
- O-14, O-15, D1–D5, L9, L18, and all standing protections remain binding.
- Seeds 201–203 retained as INSTRUMENT FAILURE evidence, never rerun.
- §1.1 growth-bar: diagnostic-only, non-gating, pending Rebecca's separate ruling.
- No B2 work addressed.
