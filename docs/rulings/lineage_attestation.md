# Lineage Attestation

**Repository:** `darkside73826779-ship-it/moving-origin-research`  
**Repository commit verified:** `a85ec91f22521164abd2604a1c299c74f0dd67ac`  
**Pre-migration workspace commit:** `1d13105e8163859d7972705b731ba8c24a272276`  
**File count verified:** 46  
**Verification date:** 2026-08-15

## Method

The exact Git commit objects at `a85ec91` were exported with `git archive`, avoiding working-tree checkout filters. They were compared with all entries in the supplied `repo_import_manifest.json`.

- Six files matched their expected SHA-256 hashes byte-for-byte.
- Forty text files contained CRLF line endings in the imported Git objects where the pre-migration manifest expected LF.
- For each of those forty files, the byte-size difference exactly equaled its number of CRLF sequences.
- After CRLF-to-LF normalization, every one of the forty files matched its expected SHA-256 hash exactly.
- The six byte-identical files were not normalized or altered.
- No unmapped files, missing files, or substantive content differences were found.

The line-ending conversion was therefore treated as a documented repository-import transport difference under Rebecca's direct instruction to use the comparison method that works without pull/checkout-induced ambiguity. The previously documented `e1_spec.md` changelog-reference rewrite remains the sole intentional semantic-text edit in the import mapping.

## Attestation

The imported tree at `a85ec91` is content-identical to the pre-migration tree at `1d13105e`, subject to two documented repository-import exceptions:

1. Forty text files were committed with CRLF line endings instead of the LF bytes represented by the pre-migration SHA-256 manifest; all forty match exactly after CRLF-to-LF normalization.
2. `e1_spec.md` rewrites the changelog reference from the absolute path `/home/user/workspace/e1_spec_CHANGES.md` to the relative path `e1_spec_CHANGES.md`.

No other discrepancies were found.
