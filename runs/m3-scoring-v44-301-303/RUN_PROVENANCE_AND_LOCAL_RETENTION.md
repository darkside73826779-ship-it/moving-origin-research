# M3 V4.4 Run Provenance and Local Artifact Retention

## Execution provenance

This scoring run was executed from repository commit
`95440b4792d1eb100b3b1d015eb02b6dbf92ecc3` using the command:

```text
python src/m3_harness.py --law all --seeds 301,302,303 --mode scoring --verify-reproducibility --output-dir ./m3_scoring_output
```

The supervised scoring prompt explicitly authorized three local execution
edits to `src/m3_harness.py` before the run:

```python
SCORING_SEEDS = [301, 302, 303]
RETAINED_INSTRUMENT_FAILURE_SEEDS = frozenset({201, 202, 203})
```

and:

```python
if mode == 'scoring':
    return set(SCORING_SEEDS)
```

These edits authorized only fresh scoring seeds 301–303 while keeping retained
instrument-failure seeds 201–203 permanently blocked. No other harness code,
bars, controls, constants, or scoring logic was changed. The edits were local
run prerequisites and are not included as a proposed source change on this
results branch.

- Base `src/m3_harness.py` Git blob: `6374359b1dec48d01c49cbc9d256350995abe039`
- Executed `src/m3_harness.py` SHA-256: `408450a59aa5bf6354503317412ff62673c5f34c5a5919acccb1bf562d588d60`

## Files retained locally

The following large artifacts were deliberately not uploaded to GitHub. They
remain preserved locally and are available upon request.

| Retained item | File count | Total bytes | Description |
|---|---:|---:|---|
| `m3_v44_raw/objects/` | 230,609 | 15,968,696,189 | Raw artifact objects, primarily binary arrays |
| `m3_v44_raw/draws/` | 27,027 | 286,596,977 | Per-draw JSON metadata |
| **Raw artifact subtotal** | **257,636** | **16,255,293,166** | Complete uncurated raw artifact tree |
| `m3_v44_raw_manifest.json` | 1 | 201,997,364 | Harness-generated index for the raw artifacts |

Raw artifact files by extension:

| Extension | File count | Total bytes |
|---|---:|---:|
| `.bin` | 224,600 | 15,958,234,168 |
| `.json` | 33,036 | 297,058,998 |

Additional local-only transport/execution records:

- `m3_v44_raw_manifest.json.zip` — 13,520,123-byte lossless transport
  derivative; its archived JSON content matches the original manifest's
  SHA-256 exactly.
- `m3_scoring_stdout_stderr.log` — complete captured outer console stream;
  the harness-generated `m3_run.log` is included in this run folder.
- `m3_scoring_run_status.json` — local wrapper exit-status and elapsed-time
  record; the same values are recorded in `m3_scoring_roundtrip_log.txt`.

The uploaded `m3_scoring_roundtrip_log.txt` contains the size and SHA-256 hash
of every file in the complete scoring output, including all locally retained
raw artifacts.
