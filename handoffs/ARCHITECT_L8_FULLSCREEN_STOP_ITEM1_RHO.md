# ARCHITECT STOP — L8 Full-Screen Amendment, Item 1 (Primary Metric) Not Computable from `b139749`

**Date:** 2026-08-20 · **Regime:** B (post-Entry 81; constitution v2 §5 binding) `[P4]`
**Gate served:** ARCHITECT amendment of the L8 G2–G4 minimal full-screen spec per Rebecca's directive (WORKFLOW COORDINATOR handoff, 2026-08-20) — Item 1 (primary metric).
**Status:** **STOP.** Returned to Rebecca for a ruling before any spec amendment. No spec files amended; `b139749` not modified; no new machinery introduced.

## Authority and the directive's own STOP condition

Rebecca's directive (Item 1) re-designates the screen's primary metric to the complete frozen-v2.2 any-seed scoring-verdict false-kill rate:

> **PRIMARY = `P(∃ seed s: β*_s < 0.2 OR ρ_s < 0.8)`** — the complete frozen-v2.2 any-seed scoring-verdict false-kill rate (a run fails if any seed `s` has `β*_s < 0.2` OR `ρ_s < 0.8`; both bars per seed `[BAR-Entry 11]`; any-seed aggregation; the frozen v2.2 line-44 scoring verdict).

The directive's computation constraint and escape hatch are binding:

> "the complete predicate must be computed directly from the existing per-seed ρ and β* arrays in `b139749` (direct calculation). Do NOT introduce a quorum, fallback, bootstrap, or Wilson procedure."
> "Confirm the complete predicate is computable from `b139749`'s per-seed ρ and β* arrays; **if not, STOP and report**."

## The blocking fact (verified, P6)

`b139749` (`diagnostics/l8_power_analysis.py` at `b1397498ca369067e956479e6c2bd6b0793c3e89`) does **not** compute or expose per-seed Spearman ρ. Verified by exhaustive inspection of the code at that SHA:

- Per-seed statistic: `beta_star_for_seed(d_seed)` returns `(β*_s, instrument_failure)` only — `β*_s = β_s / σ_pool,s` (slope / pooled within-dose SD). No ρ.
- Run-level: `run_level_beta_star(d_all)` returns the 5-seed mean of `β*_s`. No ρ.
- Direct rates: `false_kill_rate` = `P(5-seed mean β* < 0.2)`; `false_kill_rate_per_seed` = `np.mean(np.any(valid_ps < BETA_STAR_BAR, axis=1))` = `P(any seed β*_s < 0.2)` — **β*-predicate only** (code line 808). No ρ.
- Grep of the full file for `spearman`, `rho`, `ρ`, `corrcoef`, `pearson`, `scipy`, `kendall`, `rankdata`, `midrank` returns **no** Spearman/correlation computation. The only `np.argsort` calls (lines 333, 1192) rank queries by confidence at the coverage floor — a different operation, not a dose-response Spearman ρ.

Therefore the directive's premise — that `b139749` has "existing per-seed ρ and β* arrays" — is **false**. There are no per-seed ρ arrays. The complete predicate `P(∃ seed: β*_s < 0.2 OR ρ_s < 0.8)` is **not computable from `b139749`'s existing per-seed arrays**.

## Consequence and the decision Rebecca must make

To compute the complete frozen-v2.2 predicate, the implementation must **add** a per-seed Spearman ρ calculation (the v2.4 §8.9.1 definition — "Pearson correlation of midranks; dose ranks (1,2,3,4); tied D values receive the arithmetic mean of occupied one-based ranks; zero-variance rank vector → ρ_s undefined" — a direct, deterministic, non-resampling statistic; **not** a quorum/fallback/bootstrap/Wilson procedure). This is a new computation not present in `b139749`, plus new output/schema fields. Per the directive's authorized scope ("specification remediation and review only; no new machinery unless separately authorized"), this requires explicit authorization before the ARCHITECT specifies it.

**The clean ask for Rebecca:** authorize a direct per-seed Spearman ρ calculation for this screen — with the exact algorithm, tie rule, undefined-ρ rule, and schema changes — **or amend the directive**. The ARCHITECT does not choose between "add ρ" and "keep β*-only primary" on its own; both are Rebecca's call. No "keep β*-only" alternative is offered as a co-equal design choice here; it is the fallback only if Rebecca amends the directive.

## Why Item 3 is not started

Item 3 (geometry-list adoption from `4463cbc` §8.2; exact-`(W,N_w)` acceptance; deterministic `Q`-tie ordering; boundary-escalation rule; DRAFT PI ruling) is coupled to Item 1: the §5.4 geometry-acceptance (`meets_target` / minimum acceptable battery) and the Item 3 boundary-escalation rule both gate on the **primary metric**, which Item 1 leaves unresolved. Producing a spec whose acceptance rule gates on a primary metric that cannot yet be computed would not be a coherent, executable spec. Item 3 will proceed once Rebecca rules on Item 1.

## What was NOT done (integrity)

- No amendment to `specs/l8_g2g4_minimal_full_screen_spec.md` or its three companion files.
- No modification to `b139749`.
- No per-seed Spearman ρ calculation introduced.
- No bootstrap / Wilson / quorum / fallback machinery introduced.
- No scoring, no protected-seed access, no seeds 201–203/301–303, no G2–G4 freeze, no merge to main, no L15/L16/L17, no implementation.
- No lowering/raising/renaming/reinterpreting a locked bar. Locked bars (ρ ≥ 0.8, standardized slope ≥ 0.2, ≥3 doses, 5 seeds) `[BAR-Entry 11]` unchanged.
- The current spec on `architect/l8-g2g4-minimal-fullscreen` @ `a7b38b3` (CRITIC-cleared re-review `ab0111c`) remains the operative ARCHITECT spec; its current PRIMARY = `false_kill_rate_per_seed` (β*-only any-seed rate, a lower bound on the complete-verdict rate) is **unchanged** pending Rebecca's ruling.

## Pre-push scan attestation

This STOP artifact contains only public repo SHAs, branch/commit references, verbatim directive text, and code-verification findings. Pre-push self-scan for credentials, API keys, tokens, passwords, secrets, personal contact details, machine identifiers, private absolute paths, environment dumps, and PII: **clean — no blockers, no Rebecca-decision items, acceptable.**

## Next handoff

ARCHITECT → **Rebecca** (STOP; ruling required on Item 1). On Rebecca's ruling, ARCHITECT re-routes to fresh-context CRITIC → Rebecca (geometry-list signature) → TASK BUILDER. TASK BUILDER remains held.
