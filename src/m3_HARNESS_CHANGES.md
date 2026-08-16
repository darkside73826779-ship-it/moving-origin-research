# M3/E2 L3 Repair Proposal for CRITIC Review
- Preserved v4/v4.1 failures at SHAs ec457fc, 6ef3cce, and 76a8dd6.
- Disclosed 0.05–1.00 phase sweep; 0.20–0.30 grid region passed development.
- Fixed linear phase rule c*pi/16 was separately tested and is pending CRITIC.
- Kept 16 dimensions; state blocks now store [x_i[t], x_i[t-1]] with fixed A/B.
- Permuted channel weights now destroy channel-specific phase correspondence.
- Shuffled bound remains +0.01 but uses its same-fixture frozen comparator.
- Added five-seed predicate regression; locked bars/verdicts/other laws unchanged.
- Runtime HEAD/STATE hashes remain mandatory; no placeholders or scoring execution.
- Pending CRITIC review; hold-outs remain unexposed and no courier packet exists.
