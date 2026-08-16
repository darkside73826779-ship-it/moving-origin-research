"""Development-only arithmetic closure for M3 L1 shuffled-arm V4.3.

This script uses no experiment output and no scoring seed. It verifies only
pre-registered family-size and finite-randomization arithmetic.
"""

from fractions import Fraction


N_BINS = 5
N_SCORING_SEEDS = 3
N_NULL = 1000
N_CHECKS = N_BINS * N_SCORING_SEEDS
ALPHA_FAMILY = Fraction(1, 20)
ORDER_STATISTIC_INDEX_1BASED = 985


def main() -> None:
    old_two_sided = 1.0 - 0.95**N_CHECKS
    one_sided_only = 1.0 - 0.975**N_CHECKS

    # With 1000 null draws and the plus-one randomization p-value, rejection
    # at alpha/3 permits at most 15 null maxima >= the observation. Including
    # the observation gives the exact finite tail bound 16/1001.
    per_seed_tail = Fraction(16, N_NULL + 1)
    familywise_union_bound = N_SCORING_SEEDS * per_seed_tail

    assert N_CHECKS == 15
    assert ORDER_STATISTIC_INDEX_1BASED == N_NULL - 15
    assert per_seed_tail <= ALPHA_FAMILY / N_SCORING_SEEDS
    assert familywise_union_bound == Fraction(48, 1001)
    assert familywise_union_bound < ALPHA_FAMILY
    assert old_two_sided > 0.05
    assert one_sided_only > 0.05

    print(f"checks={N_CHECKS}")
    print(f"old_two_sided_fwfp={old_two_sided:.10f}")
    print(f"one_sided_only_fwfp={one_sided_only:.10f}")
    print(f"per_seed_tail_bound={per_seed_tail}={float(per_seed_tail):.10f}")
    print(
        "familywise_union_bound="
        f"{familywise_union_bound}={float(familywise_union_bound):.10f}"
    )
    print(f"bar={ALPHA_FAMILY}={float(ALPHA_FAMILY):.10f}")
    print("verdict=PASS")


if __name__ == "__main__":
    main()
