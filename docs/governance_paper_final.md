# One Human, Eight Roles: Constitutional Multi-Agent Governance for Solo Research

**Rebecca R. McClintic**
Independent Researcher
becca.mcclintic@gmail.com

*Preprint v1.0.1 — August 18, 2026 (corrections C1–C2; see Corrections note). Original: v1.0, August 17, 2026. All citations independently verified.*

**Scope statement (constitutional audit law L20):** Passing all laws of the governed program demonstrates temporal self-modeling competence — not awareness. This paper's own claims concern research governance only.

---

## Abstract

Solo researchers face a structural problem that no amount of individual rigor solves: the absence of institutional opposition. There is no reviewer whose job is to block progression, no data monitoring board empowered to halt a study, no colleague with standing to rule against the researcher's interests. We report a case study of a working alternative: a constitutional multi-agent governance system in which a single human principal delegates proposal, implementation, criticism, judgment, recordkeeping, integration, and execution to role-separated large language model (LLM) agents operating under a written constitution with pre-registered numerical bars, kill conditions, and a fail-closed scoring protocol. The system's distinguishing property is not that it automates research, but that it manufactures adversarial structure — and that this structure has demonstrably ruled against the principal's interests on multiple occasions, including the pre-registered termination of a companion research program and the refusal to certify a milestone in which 26 of 27 control checks passed. We describe the architecture, present the governance record as evidence, and analyze the system's principal failure modes — foremost among them correlated model error, which we argue becomes a validity-threatening rather than merely inconvenient limitation when the research subject is AI cognition itself. We conclude that the defensible claim is narrower than "autonomous AI research teams": a single human with sound scientific judgment, amplified by role-separated AI adversaries under a binding constitution, can approach institutional-grade rigor — provided the human retains every binding gate and the system's correlated blind spots are bounded by external human review.

---

## 1. Introduction

The rigor of institutional science does not come primarily from the intelligence of individual scientists. It comes from opposition: peer reviewers who can reject, data safety monitoring boards who can halt, replication attempts that can embarrass, and colleagues with the standing and incentive to say *no*. A solo researcher can match an institution's intelligence but not its adversarial structure. The predictable result is a literature of solo work that is enthusiastic, voluminous, and unfalsified — not because solo researchers are careless, but because nothing in their environment is empowered to stop them.

Large language models are typically proposed as a remedy for the *labor* half of this deficit: agents that write code, run experiments, and draft papers [Lu et al., 2024]. We report on a system built for the opposite half. In the program described here, LLM agents were deployed not primarily as workers but as *institutional roles* — a critic empowered to block, a judge bound to pre-registered criteria, a recorder maintaining an append-only provenance log — under a written constitution whose authority chain places the human principal above the constitution, the constitution above the team prompt, and the team prompt above any individual agent's judgment.

The scientific program governed by this system (an experimental investigation of moving-origin temporal indexing, summarized in §4.1) is not the subject of this paper and its object-level claims are not defended here. The subject of this paper is the governance system itself, and the empirical question it makes tractable: **can manufactured adversarial structure substitute for institutional opposition?** We argue the governance record provides qualified evidence that it can — and precise evidence about where it cannot.

Our contributions:

1. An architectural description of a constitutional multi-agent governance system for solo research, including role separation, fail-closed scoring, pre-registered kill conditions, and provenance requirements (§3).
2. A governance record as evidence: three episodes in which the system produced outcomes contrary to the principal's short-term interests, retained as permanent negatives rather than relabeled, plus one documented incident from a predecessor system (§4).
3. An analysis of failure modes, centered on correlated model error across nominally independent agent roles, with an argument that this failure mode is uniquely severe when the research topic is AI cognition (§5).
4. A deflationary but defensible framing of what such systems establish — and a concrete proposal for bounding their blind spots (§6).

---

## 2. Related Work

**Pre-registration and registered reports.** The locked-bar and kill-condition machinery adapts the logic of pre-registration [Nosek et al., 2018] and registered reports [Chambers, 2013]: analytic decisions and success criteria are fixed before data exist, removing the researcher's ability to move goalposts after seeing results. Our system extends this from *analysis plans* to *governance itself* — the protocol that decides what counts as a pass is locked, versioned, and fail-closed.

**Clinical-trial governance.** The distinction our system draws between *candidate failure* and *instrument failure* (§4.3), and the existence of a body empowered to halt a study on pre-specified grounds, echo practices from data safety monitoring boards and metrological calibration far more than from machine learning. We regard this as borrowed, not invented, and cite it as lineage.

**Adversarial AI oversight.** The role structure descends conceptually from AI safety via debate [Irving et al., 2018], in which correctness is pursued through structured opposition between AI systems rather than through a single system's judgment. Governance-by-document descends from Constitutional AI [Bai et al., 2022], though our constitution governs a research *process* rather than a model's training objective.

**Multi-agent LLM systems.** Multi-agent debate [Du et al., 2023] and LLM-as-judge evaluation [Zheng et al., 2023] supply the operational mechanics. Critically, the literature on LLM evaluator self-preference bias [Panickssery et al., 2024] documents the phenomenon we identify as our central limitation: LLM judges systematically favor outputs resembling their own, and role separation does not by itself break this correlation.

**Automated research.** The AI Scientist line of work [Lu et al., 2024] automates the *researcher* — hypothesis generation through paper writing. Our system is nearly the inverse: the human retains research direction and every binding decision, while automation supplies the *reviewers*. We consider the two approaches complementary and note that fully automated pipelines inherit the correlated-error problem in a more acute form, since generation and evaluation share a model family.

**Conceptual lineage of the object-level program.** The governed research program's central construct — a continuously updated "now" indexed to a system's own history — derives from Tulving's account of autonoetic consciousness and episodic memory [Tulving, 1985], the mental-time-travel literature [Suddendorf & Corballis, 2007], Husserl's analysis of the thick present with retention and protention [Husserl, 1893–1917/1991], and temporal depth in active inference [Friston, 2018]. These are cited here for completeness; the object-level program documents them independently.

---

## 3. System Design

### 3.1 Authority chain and roles

The system operates under a written constitution (twenty constraint-laws in four sections: component, interface, integration, and audit laws) with a declared authority chain: **Principal > constitution > team prompt > agent judgment**. Eight roles are separated:

- **Principal** (human) — approves specifications, numerical bars, scoring authorization, constitutional amendments, and all merges to the governed historical record. No agent may speak for the Principal.
- **ARCHITECT** — proposes specifications and experimental designs.
- **TASK BUILDER** — implements only against reviewed task specifications.
- **CRITIC** — adversarially reviews specifications, code, and results; may block progression; pre-registers objections to the constitution's own measurability.
- **JUDGE** — scores returned evidence against locked bars and kill conditions only, exclusively from raw returned artifacts, never from any agent's characterization of them.
- **RECORDER** — maintains the append-only provenance log ("If it is not in this log, it did not happen").
- **INTEGRATOR** — maintains tracked state and packages work between roles.
- **Local executor** — performs authorized runs from named commits and returns raw outputs, including failures.

Standing prohibitions were recorded at charter: no building before the measurement harness exists; no integration claim without an ablation matrix; no renaming of negatives; no agent speaking for the Principal.

### 3.2 Fail-closed scoring

The scoring harness is designed to refuse to run: in scoring mode, the set of permitted seeds is empty by default, and enabling fresh seeds requires documented, Principal-attested edits whose diffs are recorded in the run's provenance file and verified by the JUDGE against the attested commit. Seeds consumed by a failed or instrument-failed run are permanently retired to a retained-failure set and blocked from reuse, preventing silent re-rolls.

### 3.3 Verdict taxonomy

The protocol distinguishes outcomes that most research pipelines conflate:

- **PASS / FAIL** — the candidate against pre-registered bars.
- **INSTRUMENT FAILURE** — the *apparatus* (typically a control calibration) failed a pre-registered check, rendering the affected law unscoreable regardless of candidate performance. Any law-level instrument failure blocks an overall pass.
- **Kill conditions** — pre-registered results that terminate a line of investigation entirely, with the negative retained and never relabeled.

### 3.4 Provenance requirements

Every scoring run must return: a manifest with SHA-256 hashes of all summary files, a round-trip log inventorying every raw artifact (257,636 files for the most recent run), the attested commit hash, and documentation of any authorized deviations. Large evidence retained outside the public repository must have a committed inventory, checksums, a retention statement, and a request route. Repository history is never rewritten; corrections are prospective.

---

## 4. The Governance Record as Evidence

The claim that a governance system "works" is unfalsifiable if the system has only ever agreed with its principal. The evidence that matters is the record of rulings *against* interest. Three episodes and one documented incident from a predecessor system.

### 4.1 Context: the governed program

The object-level program tests whether a moving-origin temporal self-index — a continuously updated "now" reference — is operationally distinguishable within a pre-registered six-arm control battery — frozen-origin, shuffled-cadence, oracle-index, fair-naive, empty, and wall-clock-injection arms — under pre-specified tests. The program explicitly disclaims consciousness, awareness, and AGI framing; the constitution's audit laws make this disclaimer binding on all agents. Two milestones passed their gates: M1 (harness validation) and E1 (candidate correctness, operational distinctness, and load-bearing coupling on five seeds, with oracle agreement 1.0 and approximately constant candidate latency against ~6.89× growth in a fair-naive baseline). These passes are context, not evidence for the governance claim — passes are what a broken governance system would also produce.

### 4.2 Episode 1: Pre-registered termination of a companion program

A companion research program (a "glial substrate" architecture [McClintic, 2026, glial-substrate repository]) was terminated when its pre-registered kill conditions fired — specifically an integration-law failure in which components proved removable without mutual effect. The glial substrate program was a predecessor of some ideas that led to the program described here; its termination was not softened into a pivot: the program was closed, its negative findings extracted and retained, and the failure was subsequently written into the successor program's constitution as the named *calibration failure case* — the negative template the team must not reproduce.

**Governance significance:** A kill condition that has never fired is a decoration. This one fired, on the principal's own prior program, and the successor program was structurally inoculated with the corpse.

### 4.3 Episode 2: The M3 instrument-failure ruling

In the M3 V4.4 scoring run (fresh seeds 301–303), the candidate passed **every candidate-facing bar on all three seeds**. Laws L1, L5, and L6 passed on all seeds; L3's candidate-facing bars passed on all seeds. Of 27 pre-registered stochastic control checks, 26 passed. One failed: the L3 frozen-control calibration on seed 303, with a plus-one p-value of 12/1001 ≈ 0.012 against a per-seed threshold of 0.05/3 ≈ 0.0167.

Under the locked fail-closed protocol, that single apparatus failure rendered L3 unscoreable on seed 303 and blocked an overall M3 pass. The JUDGE's verdict — **INSTRUMENT FAILURE** — was published as the governing result, with an explicit interpretation note preserving both facts: the candidate did not fail, and the milestone did not pass.

**Governance significance:** This is the sharpest test in the record. The gap between the observed p-value and the threshold is small; the temptation to argue "26 of 27, and the miss was marginal, and it was a *control*, not the candidate" is exactly the reasoning that pre-registration exists to forbid. The system forbade it. The seeds were retired. The failure is permanent history.

### 4.4 Episode 3: Reproducibility defect handled without retroactive certification

The same M3 run separately reported `bit_identical = false` on a reproducibility check. Post-hoc diagnosis attributed this to a defect in the reproducibility *contract* (byte-level comparison where scoring-semantic comparison was intended). A two-digest semantic reproducibility architecture was implemented and CRITIC-reviewed — and the repair was explicitly barred from retroactively certifying the historical run, because no protected seed was rerun. The failed check stands in the historical artifacts.

**Governance significance:** The system distinguished *fixing the instrument going forward* from *repairing the past*, and refused the second even when the first was complete. This is the "no relabeled negatives" prohibition operating on a subtle case.

### 4.5 Supplementary incident: silent model substitution (predecessor system)

In a predecessor system operated by the same principal, a serving-stack change silently substituted a different model (a 32B parameter model in place of the vetted 27B model) behind an unchanged interface, producing confidently defended confabulation downstream. The incident was diagnosed by the principal, and cryptographic preflight checks (SHA-256 verification of model weights before any session) were made a permanent, modeless requirement. This episode predates the public repository and is documented in the predecessor system's internal logs.

**Governance significance:** Role separation assumes you know *which model* occupies a role. This episode demonstrates that identity verification of the agents themselves is a governance requirement, not an implementation detail.

### 4.6 What the record does not show

The record contains no episode in which an agent role caught an error that the correlated-error analysis of §5 predicts they would all share. This is not reassurance; it is exactly what that failure mode looks like from the inside.

---

## 5. Failure Modes and Limitations

### 5.1 Correlated model error (central)

The CRITIC and JUDGE are LLM instances drawn from overlapping training distributions, initialized with framing documents written within the program, and unable to resign. Role separation demonstrably reduces certain error classes — the record shows blocked progressions and adverse rulings — but it cannot break correlations inherited from shared pretraining. The documented self-preference bias of LLM evaluators [Panickssery et al., 2024] gives this concern an empirical footing.

For most research topics, correlated error is a quantitative degradation: the effective number of independent reviewers is smaller than the number of roles. For *this* program's topic, it is qualitative. The object-level research investigates a hypothesized missing component of temporal self-modeling in AI systems — evaluated by AI systems that, by hypothesis, lack that component. If current models share a systematic blind spot about temporal selfhood, every agent in the review stack shares it *in the same direction*. Human review teams have idiosyncratic biases that partially cancel; a review stack drawn from one or two model families has aligned ones. We state this as a validity condition, not a caveat: **the program's object-level conclusions cannot be certified from inside its own review stack.**

### 5.2 The Principal as single point of failure

The system's honest description is not "minimal human input." The Principal approves every specification, bar, scoring authorization, and merge; diagnosed the model-substitution incident; and chose the kill conditions that terminated the companion program. The agents supply volume and opposition; the human supplies the load-bearing judgment at every gate. This is a force multiplier for one person's scientific taste — with the corollary that the system's rigor is bounded above by that person's, and there is no mechanism inside the system that can detect the Principal's own systematic errors.

### 5.3 Governance mass

The apparatus is heavy: eight roles, an append-only provenance log, lineage attestations, a public-repository policy with its own changelog, and a 16.3 GB raw artifact tree for a single scoring run. Governance that prevents self-deception can itself become the product, consuming effort that the object-level science needs. We do not resolve this trade-off; we flag that any adopter should measure the ratio of mechanism-work to certification-work and treat its inversion as a warning sign.

### 5.4 Unattributed code lineage

Implementation code was substantially machine-generated. LLM-generated code can reproduce patterns, idioms, and occasionally near-verbatim structures from training data without an attribution trail, and neither the Principal nor the agents can rule this out by inspection. The program's response is disclosure plus a targeted audit (searching distinctive function bodies and unusual constants against public code search), performed 2026-08-17 with no verbatim reproductions of external code identified; any future findings are recorded under the repository's NOTICE per its license. Absence of findings is not absence of lineage; the disclosure stands regardless of audit outcome.

### 5.5 Gaps in the public record

The original constitution and initial decision sheet are not persisted as standalone public files; the adopted requirements are traceable only through the provenance log, state record, specifications, and rulings. The program documents this as a limitation rather than concealing it, and the defensible verification claim is correspondingly narrower. The full raw artifact tree is retained locally rather than durably hosted, with a committed inventory and request route as interim measures.

---

## 6. Discussion

### 6.1 What is actually established

The evidence supports a deliberately narrow claim: **a single human with sound scientific judgment, amplified by role-separated AI agents under a binding constitution with pre-registered bars and fail-closed protocols, can produce governance behavior — adverse rulings, retained negatives, refused certifications — characteristic of institutional science.** It does not establish that AI teams can conduct research with minimal human input; the record shows the opposite, with the human as the irreplaceable element at every binding gate. It does not establish the object-level scientific claims of the governed program, whose certification requires review uncorrelated with the machinery that produced them.

### 6.2 The recursion problem

The long-term motivation for systems like this is recursive: AI agents participating in research on architectures that may become components of future AI systems. We caution that this is precisely the regime where §5.1 stops being a limitation and becomes the central threat. A review structure whose members share the blind spots of the systems under study will pass flawed designs *fluently* — with well-formatted rulings and green dashboards. The version of the recursive future worth building is one in which the review structure can catch the reviewers' own blind spots, and no purely intra-family agent architecture achieves this. The requirement is structural: at least one reviewer whose errors are uncorrelated with the model family — today, that means a human expert outside the program; eventually, perhaps, genuinely heterogeneous model lineages.

### 6.3 Proposed external validity protocol

We commit the program to the following, in order: (1) this paper and the object-level results submitted to adversarial human review by at least one domain expert in memory research or ML systems with no stake in the program; (2) independent recomputation from the retained raw artifact tree by a party outside the program; (3) resolution of the L3 control calibration prospectively, on fresh seeds, before any newly authorized scoring; (4) durable third-party hosting of raw evidence with an accession identifier. Until (1) and (2) are complete, all green results in the program should be read with the §5.1 qualifier attached.

---

## 7. Conclusion

Institutions make science rigorous by opposing scientists. We have described a system that manufactures that opposition for a researcher who has no institution, and presented a governance record — a terminated program, a refused near-pass, an un-relabeled reproducibility failure, and a documented model-substitution incident from a predecessor system — as evidence that the opposition is real rather than decorative. The system's honest limits are equally clear: it multiplies one human's judgment rather than replacing it, and its reviewers share correlated blind spots that no amount of role separation can break from inside. The next reviewer this program needs is not another agent. It is a person with no reason to want the results to be true.

---

## Acknowledgments and AI Contribution Disclosure

AI systems (Anthropic Claude models, including agent deployments via the program's execution infrastructure) contributed to drafting specifications, implementing code, performing role-separated criticism and judgment, maintaining provenance records, and drafting this manuscript. All binding decisions, numerical bars, scoring authorizations, and merges to the historical record were made by the human author. AI-generated output is not treated as independent scientific validation. This manuscript itself was drafted with AI assistance and revised under the program's review procedure; it should be read with the same §5.1 qualifier it describes.

---

## References

Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.

Chambers, C. D. (2013). Registered Reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609–610.

Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. arXiv:2305.14325.

Friston, K. (2018). Am I Self-Conscious? (Or Does Self-Organization Entail Self-Consciousness?). *Frontiers in Psychology*, 9, 579.

Husserl, E. (1893–1917/1991). *On the Phenomenology of the Consciousness of Internal Time*. Trans. J. B. Brough. Kluwer.

Irving, G., Christiano, P., & Amodei, D. (2018). AI Safety via Debate. arXiv:1805.00899.

Lu, C., et al. (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv:2408.06292.

McClintic, R. R. (2026). Moving Origin Research [repository]. https://github.com/darkside73826779-ship-it/moving-origin-research

McClintic, R. R. (2026). Glial Substrate [repository]. https://github.com/darkside73826779-ship-it/glial-substrate

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *PNAS*, 115(11), 2600–2606.

Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM Evaluators Recognize and Favor Their Own Generations. arXiv:2404.13076.

Suddendorf, T., & Corballis, M. C. (2007). The evolution of foresight: What is mental time travel, and is it unique to humans? *Behavioral and Brain Sciences*, 30(3), 299–313.

Tulving, E. (1985). Memory and consciousness. *Canadian Psychology*, 26(1), 1–12.

Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. arXiv:2306.05685.

---

## Data Availability

The governed research program's public repository, including specifications, implementation code, test suites, scoring summaries, rulings, provenance records, and the public-repository operating policy, is available at https://github.com/darkside73826779-ship-it/moving-origin-research. The companion glial substrate repository is available at https://github.com/darkside73826779-ship-it/glial-substrate. Raw scoring artifacts (257,636 files, ~16.3 GB) are retained locally; a committed inventory with checksums and access procedures is provided in the repository. Correspondence: becca.mcclintic@gmail.com.

---

## Corrections (v1.0.1, 2026-08-18)

**C1 (§4.1, per audit finding F2).** v1.0 stated E1's controls as "frozen, naive, shuffled, permuted, and oracle." The versioned-law compliance audit (audits/AUDITOR_RETURN_HANDOFF.md, finding F2) established that the E1 battery comprised six arms with no distinct permuted arm; the control list is corrected to the battery as run. E1's verdict is unaffected; the F2 process finding (waiver never memorialized) is dispositioned separately at Gate 0.

**C2 (header, per audit finding F6).** The scope statement required by constitutional audit law L20 to appear first in any external writeup was present in v1.0 only within §4.1; it is added to the paper's opening.

Both corrections repair statements inaccurate at the time of v1.0's publication; no result, verdict, or argument is modified. Corrections are prospective; v1.0 is preserved in repository history.
