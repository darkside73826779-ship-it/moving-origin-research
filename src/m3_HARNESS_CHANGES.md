# M3/E2 L3 v4.1 Repair Record
- v4 diagnostic retained: old generator failed oracle ceiling on all seeds 101–105.
- Applied cleared AR(0.3,-0.2,0.1), period-7 sinusoid, variance 0.05, burn-in 100.
- Provenance now resolves real HEAD and STATE.md SHA-256 or aborts; no placeholders.
- Aligned oracle fit with verifier by excluding undefined 3-lag origins 0–1.
- Seed 101 failed: candidate h1/h3/h4; permuted h2/h5; shuffled h1/h3/h4/h5.
- Seed 102 failed: candidate h1/h3/h4; permuted h2/h5; shuffled h1/h3/h4.
- Seed 103 failed: candidate h1/h3/h4; permuted h2/h5; shuffled h1–h5.
- Seed 104 failed: candidate h1/h3/h4; permuted h2/h5; shuffled h1/h3/h4/h5.
- Seed 105 failed: candidate h1/h3/h4; permuted h2/h5; shuffled h1–h5; SPEC BLOCK.
