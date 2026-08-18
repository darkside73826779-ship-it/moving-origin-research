# CRITIC Review — Governance Paper Draft v1

**Paper:** "One Human, Eight Roles: Constitutional Multi-Agent Governance for Solo Research"
**Author:** Rebecca R. McClintic
**Date:** 2026-08-17
**Verdict:** BLOCK (1 blocking finding, 3 [VERIFY] tags requiring resolution)

---

## Citation verification

All 13 references independently verified against actual publications:

| # | Citation | arXiv/DOI | Status |
|---|---|---|---|
| 1 | Bai et al. (2022), Constitutional AI | arXiv:2212.08073 | VERIFIED |
| 2 | Chambers (2013), Registered Reports | Cortex, 49(3), 609-610 | VERIFIED |
| 3 | Du et al. (2023), Multiagent Debate | arXiv:2305.14325 | VERIFIED |
| 4 | Friston (2018), Am I Self-Conscious? | Front. Psychol., 9:579 | VERIFIED |
| 5 | Husserl (1893-1917/1991), Internal Time | Brough trans., Kluwer | VERIFIED |
| 6 | Irving et al. (2018), AI Safety via Debate | arXiv:1805.00899 | VERIFIED |
| 7 | Lu et al. (2024), The AI Scientist | arXiv:2408.06292 | VERIFIED |
| 8 | McClintic (2026), Moving Origin Research | GitHub repository | VERIFIED |
| 9 | Nosek et al. (2018), Preregistration Revolution | PNAS, 115(11), 2600-2606 | VERIFIED |
| 10 | Panickssery et al. (2024), LLM Self-Preference | arXiv:2404.13076 | VERIFIED |
| 11 | Suddendorf & Corballis (2007), Mental Time Travel | BBS, 30(3), 299-313 | VERIFIED |
| 12 | Tulving (1985), Memory and Consciousness | Canadian Psych., 26(1), 1-12 | VERIFIED |
| 13 | Zheng et al. (2023), LLM-as-a-Judge | arXiv:2306.05685 | VERIFIED |

All titles, authors, years, journal names, volumes, and arXiv identifiers match. The paper's own note ("arXiv identifiers and page numbers were produced from the drafting model's memory and must be independently verified") is now resolved: all identifiers are correct.

---

## Blocking findings

### BF1 — Artifact file count discrepancy (§3.4)

**Paper states:** "a round-trip log inventorying every raw artifact (257,647 files for the most recent run)"

**Repo record:** The README.md, REPRODUCING.md, and RUN_PROVENANCE_AND_LOCAL_RETENTION.md all consistently state **257,636** files. The paper's figure of 257,647 is 11 files higher.

**Required fix:** Change 257,647 to 257,636 to match the authoritative repo record.

---

## [VERIFY] tag resolution

### §3.2 — `_allowed_seeds_for_mode` characterization — RESOLVED (verified from code)

**Paper claims:** "in scoring mode, the set of permitted seeds is empty by default, and enabling fresh seeds requires documented, Principal-attested edits whose diffs are recorded in the run's provenance file and verified by the JUDGE against the attested commit"

**Code verification (at `9ae795f`, `src/m3_harness.py`):**
```python
def _allowed_seeds_for_mode(mode):
    if mode == 'development':
        return set(DEVELOPMENT_SEEDS)
    if mode == 'scoring':
        return set()  # Fail closed rather than exposing any retained seed.
    raise ValueError(f'Unsupported run mode: {mode}')
```

Also verified: `RETAINED_INSTRUMENT_FAILURE_SEEDS = frozenset(SCORING_SEEDS)` blocks seed reuse, and the main() function checks `if s in RETAINED_INSTRUMENT_FAILURE_SEEDS` and exits with an error if a retained seed is attempted.

**Verdict:** Characterization is accurate. [VERIFY] tag can be removed.

### §4.2 — Glial substrate companion program — REQUIRES REBECCA DECISION

**Paper claims:** A companion program ("glial substrate") was terminated when pre-registered kill conditions fired. The [VERIFY] tag asks whether the public repo's characterization is sufficient or whether the glial repo's kill-condition documents should be cited directly.

**CRITIC assessment:** Cannot verify from the moving-origin-research repo. The project wiki references "Glial Substrate" as a related project under Rebecca's portfolio. Rebecca must decide: (a) cite the glial repo directly, (b) keep as-is with the public repo as sole reference, or (c) cut the episode to a footnote.

### §4.5 — Model substitution episode — REQUIRES REBECCA DECISION

**Paper claims:** A predecessor system had a silent model substitution (32B replacing 27B). The [VERIFY] tag notes this predates the public repository and asks whether to include it or cut to a footnote.

**CRITIC assessment:** Cannot verify from any public artifact. Rebecca must decide: (a) include with artifact references she can produce, (b) cut to a footnote, or (c) remove entirely.

---

## Non-blocking findings

### NF1 — "OpenClaw" not referenced in repo

The acknowledgments mention "agent deployments via OpenClaw." This term does not appear in any public repo file. If "OpenClaw" is an internal platform name, it may need context for outside readers per the public-readable writing standard. If it's a product name, verify it's correctly spelled.

### NF2 — Constitution law count and sections

The paper states "twenty constraint-laws in four sections: component, interface, integration, and audit laws." The 20-law count matches the project description. The four section names cannot be verified from the public repo (the constitution itself is noted as not persisted as a standalone public file, per §5.5). This is consistent with the paper's own §5.5 acknowledgment.

### NF3 — L20 reference

The paper states "the constitution's audit law L20 makes this disclaimer binding on all agents." The harness code has `l20_self_test` which is a drift detection function, not a claims-boundary law. These may be different aspects of the same law number, or the constitution's L20 may differ from the harness's L20. The paper should clarify whether constitution L20 and harness L20 are the same law or different.

### NF4 — "approximately 6.9×" rounding

The repo says "approximately 6.89×" and the paper says "approximately 6.9×." This rounding is acceptable but the more precise figure could be used for a research paper.

---

## Claims discipline assessment — PASS

The paper demonstrates excellent claims discipline:

1. **Proper scoping:** "The scientific program governed by this system... is not the subject of this paper and its object-level claims are not defended here." The paper is about governance, not the science.

2. **M1/E1 as context, not evidence:** "These passes are context, not evidence for the governance claim — passes are what a broken governance system would also produce." This is the right framing.

3. **M3 accurately described:** INSTRUMENT FAILURE with all details matching the repo. The 26/27 controls, the p-value, the threshold, the seed retirement — all verified accurate.

4. **No consciousness/AGI overclaiming:** "The program explicitly disclaims consciousness, awareness, and AGI framing." The conceptual lineage citations are framed as lineage, not as supporting consciousness claims.

5. **Honest limitations:** §5 (failure modes) is the strongest section. Correlated model error is stated as the central limitation, not a footnote. The §5.1 argument that the limitation is qualitative (not just quantitative) for this specific research topic is well-reasoned.

6. **Deflationary conclusion:** "a single human with sound scientific judgment, amplified by role-separated AI agents... can approach institutional-grade rigor" — uses "approach" not "achieve" or "replace." The final sentence is exactly right: "The next reviewer this program needs is not another agent. It is a person with no reason to want the results to be true."

7. **Reproducibility episode (§4.4):** Accurately describes the construction bug, the two-digest fix, and the refusal to retroactively certify. Matches the repo record.

---

## Alignment with research record — PASS

- Eight roles match the repo's governance description ✓
- Authority chain (Principal > constitution > prompt > judgment) matches ✓
- Fail-closed scoring verified from code ✓
- INSTRUMENT FAILURE taxonomy matches ✓
- Provenance requirements match ✓
- 16.3 GB artifact tree matches ✓
- No scientific bars, predicates, or verdicts modified ✓

---

## Verdict: BLOCK

One blocking finding (file count error) and two [VERIFY] tags requiring Rebecca's decision. The paper is otherwise excellent — claims discipline is strong, citations are all verified, and the governance record is accurately represented. The file count is a trivial fix; the [VERIFY] tags are Rebecca's prerogative.

---

## Next steps

1. **BF1:** Change 257,647 → 257,636
2. **[VERIFY] §4.2:** Rebecca decides on glial substrate citation
3. **[VERIFY] §4.5:** Rebecca decides on model substitution episode
4. **[VERIFY] §3.2:** Tag can be removed — verified from code
5. **NF1-NF4:** Address at Rebecca's discretion before external circulation
