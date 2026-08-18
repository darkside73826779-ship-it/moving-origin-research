# ARCHITECT Combined Handoff — BF1 Remediation (Task A) + L3 Sequencing Options (Task B)

**Gates served:** (A) BF1 remediation per CRITIC R2 BLOCK; (B) Step 4 of Principal's M4 gate resolution sequence
**Issued by:** ARCHITECT
**Date:** 2026-08-18 19:30 EDT
**Regime:** B (post-Entry 27; constitution v1 + Amendment 1; §5 binding) (P4)
**Base SHA:** `956a5e7` (GitHub main, verified)

---

## TASK A — BF1 remediation

**Branch:** `architect/m4-spec-v1.3`
**New HEAD SHA:** `b3165061f876a84ac83eec33b15885d51b384e83` (verified via `git ls-remote`)
**Previous HEAD:** `c0a3413` (BF1/NF1 from prior cycle)

### BF1 fixes applied (tags only, no value changes)

| # | Location | What was untagged | Tag applied |
|---|---|---|---|
| BF1.a | §3.3 (line 133) | "≥ 1" homeostatic variable lower bound | `[LAW-L8]` (verbatim: "At least one homeostatic variable…") |
| BF1.b | §3.4 (lines 150–157) | All six L8 control-arm failure routings | Added Source column: 5× `[PROPOSED — requires Rebecca sign-off]`, 1× `[LAW-L8]` (frozen KILL = "stakes decorative" is law text) |
| BF1.c | §9.2 (lines 348–349) | Tripwire values "2" (sessions) and "4" (days) | `[PROPOSED — requires Rebecca approval]` |

### NF annotations applied (optional, recommended by CRITIC)

| NF | Disposition |
|---|---|
| NF1 | No change needed — CRITIC verified L14 quote is byte-identical (trailing space is constitution whitespace artifact) |
| NF2 | Added citation to M3 implementation entries for V4.4 alpha_seed specifics |
| NF3 | Annotated [BAR-Entry 11.8] as (gate-decision) source class in §2.2 |
| NF4 | Annotated §7.1 "1 pool" and "45" as [PROPOSED — derived] quantities |

### Changelog updated

`specs/m4_specification_changelog.md` — new v1.3.1 entry documenting all BF1 and NF fixes.

### Confirmation

No threshold value, bar, kill condition, or scoring predicate changed. Only source-class tags and annotations added. No law text modified. No reconstruction.

**Next recipient:** CRITIC (R2 re-review of the tag delta).

---

## TASK B — L3 sequencing contradiction options

**Branch:** `architect/l3-sequencing-options`
**HEAD SHA:** `29e02ecf3c86cd327b8593abd132ae5836b9e121` (verified via `git ls-remote`)
**File:** `docs/options/l3_sequencing_options.md`

### The contradiction

- **Governance paper §6.3(3)** (line 165): "resolution of the L3 control calibration prospectively, on fresh seeds, before any newly authorized scoring"
- **M4 spec §8** (line 318): L3 disposed as "Parallel, not blocking"
- An M4 scoring run is "newly authorized scoring" → conflict.

### Option A (advisor lean) — Amend spec §8

M4 build proceeds in parallel; M4 scoring gated on prospective L3 resolution on fresh seeds. Keeps governance paper's public pre-registration commitment intact. Cost: potential scoring delay.

### Option B — Amend governance paper §6.3

Public amendment allowing M4 scoring before L3 resolution with a published qualifier. Rationale: M4 tests different laws (L7/L8/L10/L14/L18) than L3. Cost: public deviation from pre-registered protocol.

### Comparison

| Dimension | Option A | Option B |
|---|---|---|
| What changes | M4 spec §8 (internal) | Governance paper §6.3 (public) |
| Pre-registration impact | None | Public amendment |
| M4 build | Unaffected | Unaffected |
| M4 scoring | Gated on L3 | Not gated |
| Governance paper | Intact | Amended |
| ARCHITECT recommendation | Yes | No |

### Draft only

No option implemented. Rebecca rules.

**Next recipient:** Rebecca (RULING).

---

## SHAs

| Item | SHA | Branch |
|---|---|---|
| GitHub main HEAD | `956a5e7` | main |
| Task A spec HEAD | `b3165061f876a84ac83eec33b15885d51b384e83` | architect/m4-spec-v1.3 |
| Task B options HEAD | `29e02ecf3c86cd327b8593abd132ae5836b9e121` | architect/l3-sequencing-options |

---

## Explicitly prohibited (both tasks)

- No merging to main (Rebecca sole merge authority)
- No scoring, seed execution, or hold-out seed exposure
- No rerun of seeds 201–203 / 301–303 (O-14)
- No L15/L16/L17 work before M5
- No modification of STATE.md or provenance_log.md
- No renaming, reinterpreting, or silently replacing any negative result or INSTRUMENT FAILURE label
- No implementation of either Task B option (draft only)
