# Local Artifact Inventory

Verified on 2026-08-17. The raw artifacts described here are retained on local storage and are not stored in this GitHub repository.

## Retained scoring runs

| Scoring run | Seeds | Locally retained material | File count | Byte count | SHA-256 |
|---|---|---|---:|---:|---|
| `M3-SCORING-1` | 201–203 | Governed scoring output package (`m3_manifest.json` and nine associated summary, log, profile, and ledger files) | 10 | 1,780,758 | `C1FF468733D514692AE4895344A6B8A69CA515C88F9EB0AFDD3341E6C1F38B5F` (`m3_manifest.json`) |
| `M3-SCORING-2` | 301–303 | Complete V4.4 raw artifact tree | 257,636 | 16,255,293,166 (16.3 GB decimal) | `C5C4D6F2156627F87058B23942A9F9728F3C9293352AC341A20E9514772D7C3E` (`m3_v44_raw_manifest.json`) |

The `M3-SCORING-2` scoring-run manifest (`m3_manifest.json`) has SHA-256 `9E8C875A5B435DC7CB1F2B00A556289CC86A9FF5507B0E5468D1848DC4F3851B`.

`M3-SCORING-1` predates the V4.4 raw-artifact format and therefore has no corresponding `m3_v44_raw/` tree. Its governed returned outputs remain retained under their original verdict.

## Retention

Seeds 201–203 and 301–303 are retained scoring evidence and must never be rerun. The O-14 prohibition on rerun-on-failure remains binding. Retention does not change either run's historical verdict or authorize new scoring.

The 301–303 raw tree is retained in a primary local preservation location and a separate local archive copy. A parallel verification checked all 257,636 raw files against the V4.4 manifest by byte length and SHA-256 and passed on 2026-08-17.

## Access procedure

To request access, open a GitHub issue labeled as an artifact-access request. Identify the requested scoring run, files, intended use, and preferred secure transfer method. Do not place credentials, private system information, or security-sensitive material in the public issue.

Access is coordinated by the project custodian. Any transferred package should be verified against the SHA-256 values above. The raw artifacts will not be committed to GitHub.
