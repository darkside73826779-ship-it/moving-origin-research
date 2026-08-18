# ARCHITECT Draft — §6.3/L3 Sequencing Contradiction: Options for Rebecca's Ruling

**Step served:** Step 4 of Principal's M4 gate resolution sequence
**Issued by:** ARCHITECT
**Date:** 2026-08-18 19:24 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Base SHA:** `956a5e7` (GitHub main)
**Branch:** `architect/l3-sequencing-options`
**Status:** DRAFT ONLY — Rebecca rules. No option is implemented.

---

## The contradiction

**Governance paper §6.3** (`docs/governance_paper_final.md`, line 165) commits the program to, in order:

> "(3) resolution of the L3 control calibration prospectively, on fresh seeds, before any newly authorized scoring;"

**M4 spec §8** (`specs/m4_specification.md`, line 318) disposes L3 as:

> "L3 control calibration resolution | Parallel | M3 L3 issue; M4 tests different laws. Parallel, not blocking."

**Conflict:** An M4 scoring run is "newly authorized scoring." The governance paper says L3 must be resolved on fresh seeds before any newly authorized scoring. The M4 spec says L3 is parallel and not blocking — implying M4 scoring could proceed before L3 is resolved.

---

## Option A — Amend spec §8 (scoring gated on L3 resolution)

**Advisor lean.** Keeps the governance paper's commitment intact.

### Proposed spec §8 amendment

Replace the L3 row in §8 with:

> | L3 control calibration resolution | Prerequisite for scoring | M3 L3 issue; M4 tests different laws. Build (implementation, diagnostic runs) proceeds in parallel. M4 scoring is gated on prospective L3 calibration resolution on fresh seeds, per governance paper §6.3(3). |

Add to §8 a new row or note:

> **Sequencing note:** Per governance paper §6.3(3), no M4 scoring run is authorized until L3 control calibration is resolved prospectively on fresh seeds. M4 build (TASK BUILDER implementation, diagnostic runs under O-15) proceeds in parallel with L3 calibration work. The gate sequence is: (1) L3 resolution on fresh seeds; (2) M4 scoring authorization via Rebecca's courier channel; (3) M4 scoring execution.

### Rationale

- The governance paper is the program's public commitment to external validity. Its ordering is a pre-registration — changing it requires a public amendment with rationale, which is more disruptive than adjusting an internal spec.
- L3 and M4 test different laws (L3 = continuous invariant; M4 = L7/L8/L10/L14/L18). Build work for M4 can proceed immediately since diagnostic runs (O-15) are not "newly authorized scoring."
- The cost of Option A is a potential delay to M4 scoring if L3 resolution takes time. The cost of Option B is a public deviation from a pre-registered external-validity protocol.
- The governance paper's commitment is to external validity — the order exists so that if L3 resolution reveals an instrument problem, M4 scoring isn't built on a compromised foundation. This is defensible even though M4 tests different laws, because L3 (continuous invariant) is a cross-cutting interface law that could affect instrument integrity.

### What it preserves

- Governance paper §6.3 ordering intact (no public amendment needed)
- Pre-registration commitment honored
- External validity protocol unchanged

### What it changes

- M4 spec §8: L3 disposition changes from "Parallel, not blocking" to "Prerequisite for scoring; build parallel"
- M4 scoring timeline: scoring cannot begin until L3 is resolved on fresh seeds
- M4 build timeline: unaffected (implementation and diagnostic runs proceed)

### Impact on M4 timeline

- **Build:** Proceeds immediately. TASK BUILDER can implement the M4 harness, run diagnostic seeds (O-15), and prepare for scoring.
- **Scoring:** Waits for L3 resolution. If L3 resolution is quick, minimal delay. If L3 reveals issues requiring instrument changes, M4 scoring waits longer.
- **Net effect:** Build and L3 work happen in parallel; scoring is the gate.

### Interaction with other constraints

- **O-14 (no re-run-on-failure):** No interaction. L3 resolution is separate from M3 scoring.
- **O-15 (development diagnostic-only):** M4 diagnostic runs proceed under O-15 while L3 resolution happens in parallel. No conflict.
- **D1–D5 (Persistence Doctrine):** No interaction. Both L3 resolution and M4 scoring produce persisted artifacts regardless of ordering.
- **L18 (full battery):** No interaction. L18 applies within each milestone's scoring.
- **Hold-out seed rule (≥2 unseen seeds):** No interaction. L3 resolution and M4 scoring use different seed pools.
- **§5 P1–P6:** No interaction. The amendment is to spec §8, not to law text. No reconstruction.

---

## Option B — Amend governance paper §6.3 (public amendment)

### Proposed paper §6.3 amendment

Replace item (3) in §6.3 with:

> "(3) resolution of the L3 control calibration prospectively, on fresh seeds, before any newly authorized scoring, with the exception that M4 scoring (which tests L7, L8, L10, L14, and L18 — none of which is L3) may proceed before L3 resolution, provided that L3 resolution remains a prerequisite for any subsequent milestone scoring (M5 and beyond) and that M4 scoring results are published with an explicit qualifier that L3 resolution is pending at the time of scoring;"

### Rationale

- M4 tests different laws than L3. L3 is a continuous-invariant interface law (§2 of constitution); M4 tests mirror/stakes/retrieval-honesty/contamination (§1 and §4). There is no logical dependency between L3 resolution and M4 scoring validity.
- The governance paper's §6.3(3) was written as a general commitment. An exception for M4 is defensible because M4's test surface does not overlap with L3's domain.
- The qualifier requirement ensures transparency: M4 results are not presented as if L3 is resolved.

### What it preserves

- M4 scoring can proceed without waiting for L3 resolution
- L3 resolution remains required for M5+ milestones
- Transparency via qualifier on M4 results

### What it changes

- Governance paper §6.3: public amendment to a pre-registered external-validity protocol
- The program's public commitment is modified — this is visible to external reviewers
- Sets a precedent that the §6.3 ordering can be amended, which may weaken its force as a pre-registration

### Impact on M4 timeline

- **Build:** Proceeds immediately.
- **Scoring:** Proceeds immediately after Rebecca authorizes (no L3 gate).
- **Net effect:** No delay to M4 scoring.

### Interaction with other constraints

- **O-14:** No interaction.
- **O-15:** No interaction. M4 diagnostic runs proceed as normal.
- **D1–D5:** No interaction.
- **L18:** No interaction.
- **Hold-out seed rule:** No interaction.
- **§5 P1–P6:** The amendment is to the governance paper, not to constitutional law text. However, under P5 (deviation memorialization), this amendment should be memorialized with Rebecca's sign-off in the provenance log. The governance paper is a public document, so the amendment is itself a form of public deviation memorialization.

### Risk

- A public amendment to a pre-registered protocol may be viewed by external reviewers as moving the goalposts. The rationale (different law domains) is strong but not airtight: L3 is a continuous invariant, and its failure could theoretically indicate an instrument-level problem that affects all laws. The counter-argument is that L18 contamination controls at M4 would catch instrument-level problems independently.

---

## Comparison

| Dimension | Option A (amend spec §8) | Option B (amend paper §6.3) |
|---|---|---|
| What changes | M4 spec §8 (internal) | Governance paper §6.3 (public) |
| Pre-registration impact | None (spec is internal) | Public amendment to pre-registered protocol |
| M4 build timeline | Unaffected | Unaffected |
| M4 scoring timeline | Gated on L3 resolution | Not gated on L3 |
| Governance paper intact | Yes | No (amended) |
| Transparency | Internal (spec change) | Public (paper amendment with rationale) |
| Risk | Scoring delay if L3 takes time | Precedent of amending pre-registration |
| Advisor lean | Yes | No |

---

## ARCHITECT recommendation

**Option A.** The governance paper's §6.3(3) is a public pre-registration commitment. Amending it (Option B) has reputational cost and sets a precedent. Option A keeps the commitment intact while allowing M4 build work to proceed in parallel. The cost is a potential scoring delay, but this is preferable to weakening a pre-registered external-validity protocol.

However, ARCHITECT does not rule. Rebecca decides.

---

## Explicitly prohibited

- No implementation of either option
- No merging to main
- No scoring, seed execution, or hold-out seed exposure
- No modification of STATE.md or provenance_log.md
- No L15/L16/L17 work before M5
