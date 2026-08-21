# FORMAL HANDOFF — INCUMBENT AUTHORITATIVE ARCHITECT → WORKFLOW COORDINATOR — TOKENIZER BF1

**Timestamp:** 2026-08-21 EDT
**Work item/gate:** M4 tokenizer BF1 deterministic `.gitattributes` checkout-byte remediation
**Sender:** incumbent authoritative ARCHITECT
**Intended receiver / next owner:** WORKFLOW COORDINATOR for authoritative CRITIC rereview
**Canonical authority:** `coordinator/m4-tokenizer-bf1-manifest@24b340e5df8970d67b197830feb80e9aa612689a`
**Immutable routing input:** `critic/m4-tokenizer-nf1-nf2-rereview@6d0659b8325500596d36ae010ba203d0e40eaf8b`
**Work branch:** `architect/m4-tokenizer-bf1-remediation`

## Return

BF1 is narrowly remediated by the exact committed self-rule `.gitattributes text eol=lf`. The released commit now binds the file's mounted checkout form independently of ambient `core.autocrlf`; pre-mount verification requires `git check-attr text eol -- .gitattributes` to return `text: set` and `eol: lf`. The wrapper requires the same regular non-link mounted file to be exactly `1817` LF bytes with SHA-256 `7811d61d53e74c99543e9d796bd8857076b022c666338ce2954ef236156a4179` before parsing the self-rule and 18 exact path declarations `[PROPOSED]`.

The materialization test contract is correspondingly rebound to `6487` LF bytes, SHA-256 `93f36ebce0153068830ab471ad80d4984bd3c6ea1ef31e0f7cddf018fdad2ed5`, with its adjacent sidecar updated. NF2 and all other identities and commands remain unchanged.

## Holds and next event

The single tokenizer materialization operation remains unconsumed. Custody/model/tokenizer access; OCI materialization or inference; Q2/EF3; qualification; diagnostics/scoring; protected seeds; scientific or STATE/provenance mutation; rerun, publication, merge, and gate decision remain prohibited. Next expected event is Coordinator receipt and authoritative CRITIC BF1 rereview. Ownership transfers only on Coordinator acknowledgement.
