import unittest

import episodic_cache
import episodic_serialize
import episodic_store
import m3_harness as m3


class M3HarnessTests(unittest.TestCase):
    def test_l1_fixture_and_candidate_sets(self):
        fixture = m3._l1_build_fixture(101)
        self.assertEqual(len(fixture["autobiography"]), 2200)
        self.assertEqual(len(fixture["priming_events"]), 1200)
        self.assertFalse(fixture["has_cycle_collision"])
        sets = m3._l1_build_candidate_sets(101)
        self.assertEqual(len(sets), 100)
        counts = {idx: 0 for idx in range(200)}
        for candidate_set in sets:
            self.assertEqual(len(candidate_set), 10)
            for idx in candidate_set:
                counts[idx] += 1
        self.assertEqual(set(counts.values()), {5})

    def test_l1_v42_permuted_gate_passes_seed_102(self):
        result = m3.run_l1(102)
        self.assertEqual(result["verdict"], "PASS")
        permuted = result["permuted"]
        self.assertTrue(permuted["within_mean_pm_2sd_band"])
        self.assertTrue(permuted["null_p95_le_0_15"])
        self.assertIn(
            "diagnostic_5bin_r_squared_non_gating", permuted)
        self.assertNotIn("permuted R² outside null band", " ".join(
            result["instrument_failure_reasons"]))

    def test_l3_windows_are_disjoint_and_complete(self):
        fit_used = set(range(700))
        eval_used = set(range(705, 1005))
        for horizon in range(1, 6):
            fit_used.update(range(horizon, 700 + horizon))
            eval_used.update(range(705 + horizon, 1005 + horizon))
        self.assertFalse(fit_used & eval_used)
        self.assertEqual(fit_used | eval_used, set(range(1010)))

    def test_l3_repair_passes_all_development_predicates(self):
        for seed in m3.DEVELOPMENT_SEEDS:
            result = m3.run_l3(seed)
            self.assertEqual(result["verdict"], "PASS")
            candidate = [
                result["reductions"][str(h)] for h in range(1, 6)]
            oracle = [
                result["oracle_reductions"][str(h)] for h in range(1, 6)]
            permuted = [
                result["permuted_reductions"][str(h)]
                for h in range(1, 6)
            ]
            shuffled = [
                result["shuffled_reductions"][str(h)]
                for h in range(1, 6)
            ]
            shuffled_frozen = [
                result["shuffled_frozen_reductions"][str(h)]
                for h in range(1, 6)
            ]
            self.assertTrue(all(value >= 0.05 for value in candidate))
            self.assertTrue(
                all(0.05 < value < 0.95 for value in oracle))
            self.assertTrue(all(value <= 0.0 for value in permuted))
            self.assertTrue(all(
                observed <= frozen + 0.01
                for observed, frozen in zip(shuffled, shuffled_frozen)
            ))

    def test_l5_chain_closure_and_counting(self):
        combo = m3._l5_build_combination_fixture(101)
        facts, chains = m3._l5_build_chain_fixture(101)
        self.assertEqual(len(combo), 200)
        self.assertEqual(len(facts), 200)
        self.assertEqual(
            sum(fact["supersedes"] is not None for fact in facts), 180)
        store = m3._L5FactStore(combo, facts, chains, frozen=False)
        before = store.get_access_count_snapshot()
        path = store.walk_chain(0, 10)
        delta = store.get_access_count_snapshot() - before
        self.assertEqual(path, [f"chain_0_{idx}" for idx in range(9, -1, -1)])
        self.assertEqual(delta, 10)

    def test_l6_public_graph_is_exact(self):
        public = lambda module: {
            name for name in dir(module) if not name.startswith("_")
        }
        self.assertEqual(
            public(episodic_store),
            {"query_episodic", "query_episodic_batch"},
        )
        self.assertEqual(public(episodic_cache), set())
        self.assertEqual(
            public(episodic_serialize), {"to_json", "from_json"})

    def test_interface_negative_injections(self):
        self.assertTrue(m3.run_interface_invariants()["passes"])


if __name__ == "__main__":
    unittest.main()
