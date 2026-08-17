import inspect
import tempfile
import unittest
from unittest import mock

import episodic_cache
import episodic_serialize
import episodic_store
import m3_harness as m3
import numpy as np
from m3_v44_artifacts import RawArtifactWriter, load_array, validate_manifest


class M3HarnessTests(unittest.TestCase):
    def test_critic_b1_seed_mode_guard_static(self):
        self.assertEqual(m3.SCORING_SEEDS, [201, 202, 203])
        self.assertEqual(
            m3._allowed_seeds_for_mode("development"),
            set(m3.DEVELOPMENT_SEEDS),
        )
        self.assertEqual(
            m3._allowed_seeds_for_mode("scoring"),
            set(),
        )
        self.assertNotIn(
            201, m3._allowed_seeds_for_mode("development"))
        self.assertNotIn(201, m3._allowed_seeds_for_mode("scoring"))
        self.assertNotIn(101, m3._allowed_seeds_for_mode("scoring"))
        self.assertEqual(
            m3.RETAINED_INSTRUMENT_FAILURE_SEEDS, frozenset({201, 202, 203}))
        self.assertNotIn(999, m3._allowed_seeds_for_mode("scoring"))
        self.assertEqual(
            m3._run_type_for_mode("development"),
            "development_diagnostic",
        )
        self.assertEqual(m3._run_type_for_mode("scoring"), "scoring")

    def test_critic_b1_parser_modes_static(self):
        source = inspect.getsource(m3.main)
        self.assertIn(
            "choices=['development', 'scoring']", source)

    def test_retained_seed_is_rejected_before_dispatch(self):
        with mock.patch.object(
                m3.sys, "argv",
                ["m3_harness.py", "--law", "L1", "--seeds", "201"]):
            with self.assertRaises(SystemExit) as exited:
                m3.main()
        self.assertEqual(exited.exception.code, 1)

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
        ranks = m3._v44_l1_ranked_occurrences(
            sets, np.ones(200), list(range(200)))
        # 100 sets × 10 entries; duplicate slots are retained rather than
        # overwritten by a per-entry dictionary.
        self.assertEqual(ranks.shape, (1000, 3))

    def test_l1_v44_permuted_uses_200_entry_occurrence_statistic(self):
        fixture = m3._l1_build_fixture(101)
        sets = m3._l1_build_candidate_sets(101)
        rho, mapped, accessibility = m3._v44_l1_permuted_statistic(
            fixture["measured_entries"], sets, list(range(200)))
        self.assertTrue(np.isfinite(rho))
        self.assertEqual(len(mapped), 200)
        self.assertEqual(len(accessibility), 200)
        self.assertTrue(all(np.isfinite(value) for value in accessibility.values()))

    def test_l1_v44_shuffled_reassigns_individual_priming_queries(self):
        fixture = m3._l1_build_fixture(101)
        original = [entry["rehearsal"] for entry in fixture["measured_entries"]]
        _, assignments, counts = m3._v44_l1_priming_reassignment(
            fixture["measured_entries"], fixture,
            [6 * (index % 200) + (index // 200)
             for index in range(m3.L1_PRIMING_COUNT)],
        )
        self.assertEqual(len(assignments), m3.L1_PRIMING_COUNT)
        self.assertEqual(sum(counts), m3.L1_PRIMING_COUNT)
        self.assertNotEqual(counts, original)
        self.assertEqual(set(counts), {6})
        # Consecutive events from one original recipient are no longer bundled.
        original_recipient = fixture["priming_events"][0]["ref_global_idx"]
        original_event_positions = [
            index for index, event in enumerate(fixture["priming_events"])
            if event["ref_global_idx"] == original_recipient
        ]
        self.assertGreater(
            len({assignments[index] for index in original_event_positions}), 1)

    def test_v44_summary_is_exact_plus_one_with_ties_adverse(self):
        summary = m3._v44_summary(
            985.0,
            list(range(m3.V44_NULL_REPLICATES)),
            direction="upper",
            records=[],
        )
        # Null values 985..999 are 15 upper-tail exceedances; the plus-one
        # rank is 16/1001 and must fail the strict p > .05/3 predicate.
        self.assertEqual(summary["exceed_or_tie_count"], 15)
        self.assertEqual(summary["plus_one_p_value"], 16 / 1001)
        self.assertFalse(summary["per_seed_pass"])
        self.assertEqual(summary["alpha_seed"], 0.05 / 3)

    def test_l3_windows_are_disjoint_and_complete(self):
        fit_used = set(range(700))
        eval_used = set(range(705, 1005))
        for horizon in range(1, 6):
            fit_used.update(range(horizon, 700 + horizon))
            eval_used.update(range(705 + horizon, 1005 + horizon))
        self.assertFalse(fit_used & eval_used)
        self.assertEqual(fit_used | eval_used, set(range(1010)))

    def test_l3_v44_zero_initialization_and_absolute_burnin(self):
        innovations = np.zeros((1110, 8), dtype=np.float64)
        scored = m3._l3_sequence_from_innovations(innovations)
        self.assertEqual(scored.shape, (1010, 8))
        self.assertTrue(np.all(np.isfinite(scored)))
        # The t=0 sinusoid must be generated before burn-in, unlike the
        # legacy implementation that began its recurrence at t=3.
        phase = np.arange(8, dtype=float) * (np.pi / 16.0)
        self.assertTrue(np.allclose(
            m3._l3_sequence_from_innovations(innovations)[0],
            scored[0],
        ))
        self.assertFalse(np.allclose(scored[0], 0.0))
        self.assertTrue(np.allclose(m3._l3_v44_compute_state(scored)[0], 0.0))

    def test_v44_public_control_routes_do_not_use_numpy_rng(self):
        for function in (m3.run_l3, m3.run_l5):
            source = inspect.getsource(function)
            self.assertNotIn("RandomState", source)
            self.assertNotIn("default_rng", source)
            self.assertIn("V4.4", source)
        self.assertIn("L1_TIEBREAK_SEED", inspect.getsource(m3.run_l1))

    def test_v44_l5_route_retains_exact_control_failure_branches(self):
        source = inspect.getsource(m3.run_l5)
        self.assertIn("candidate access_count delta != k", source)
        self.assertIn("fair-naive exact world-validity accuracy != 0.75", source)
        self.assertIn("frozen post-freeze chain walk accuracy > 0", source)
        self.assertIn("shuffled chain walk accuracy > 0.05", source)
        self.assertIn("full-scan exact path accuracy/delta=200 failed", source)
        self.assertIn("shuffled query-order accuracy differs from original", source)

    def test_v44_l5_exact_helpers_reject_mutated_controls(self):
        full_scan_rows = [{
            "accuracy": 1.0, "access_count_delta": m3.L5_N_CHAIN_FACTS
        }]
        self.assertTrue(m3._v44_l5_full_scan_exact(full_scan_rows))
        full_scan_rows[0]["access_count_delta"] = 199
        self.assertFalse(m3._v44_l5_full_scan_exact(full_scan_rows))
        oracle_combo = {
            "world_validity_accuracy": 1.0,
            "self_acquisition_accuracy": 1.0,
        }
        oracle_rows = [{"accuracy": 1.0, "access_count_matches_k": True}]
        self.assertTrue(m3._v44_l5_oracle_exact(oracle_combo, oracle_rows))
        oracle_rows[0]["access_count_matches_k"] = False
        self.assertFalse(m3._v44_l5_oracle_exact(oracle_combo, oracle_rows))
        self.assertTrue(m3._v44_l5_empty_exact(
            {"error": "empty_fixture"}, {"error": "empty_fixture"}))
        self.assertFalse(m3._v44_l5_empty_exact(
            {"error": None}, {"error": "empty_fixture"}))

    def test_v44_l1_raw_draw_manifest_and_judge_recomputation(self):
        fixture = m3._l1_build_fixture(101)
        candidate_sets = m3._l1_build_candidate_sets(101)
        ranking = list(range(200))
        result = m3._v44_l1_arm(
            fixture["measured_entries"], candidate_sets, ranking)
        with tempfile.TemporaryDirectory() as directory:
            writer = RawArtifactWriter(directory)
            registry = m3.RNGDomainUseRegistry()
            derivation = m3._v44_draw(
                "L1", "frozen", "OBSERVED", 42, 0, 0, registry)
            accepted = derivation.permutation()
            reference = m3._v44_write_l1_draw(
                writer, "L1.frozen", "OBSERVED", 0,
                [derivation.artifact_record(accepted)],
                fixture["measured_entries"], candidate_sets, result, ranking)
            self.assertIn("L1_frozen_observed", reference)
            writer.finalize()
            manifest = validate_manifest(directory, require_full_family=False)
            self.assertTrue(manifest["complete_raw_schema"])
            entries = {
                item["field_name"]: item for item in manifest["arrays"]
            }
            bin_means = load_array(
                directory, entries["bin_means_5"]).reshape(-1)
            bin_ages = load_array(
                directory, entries["bin_age_representatives_5"]).reshape(-1)
            recomputed_r2 = m3._r_squared(bin_ages.reshape(-1, 1), bin_means)
            self.assertAlmostEqual(recomputed_r2, result["r_squared"], places=12)

    def test_v44_l3_raw_draw_manifest_and_reduction_recomputation(self):
        registry = m3.RNGDomainUseRegistry()
        derivation = m3._v44_draw(
            "L3", "frozen", "OBSERVED", 42, 0, 0, registry)
        innovations = derivation.gaussian_innovations()
        sequence = m3._l3_sequence_from_innovations(innovations)
        draw = m3._l3_family_draw(sequence, "frozen")
        with tempfile.TemporaryDirectory() as directory:
            writer = RawArtifactWriter(directory)
            m3._v44_write_l3_draw(
                writer, "L3.frozen", "OBSERVED", 0,
                [derivation.artifact_record()], innovations,
                sequence, draw)
            writer.finalize()
            manifest = validate_manifest(directory, require_full_family=False)
            entries = {
                item["field_name"]: item for item in manifest["arrays"]
            }
            baseline = load_array(
                directory, entries["baseline_loss_5"]).reshape(-1)
            frozen = load_array(
                directory, entries["frozen_loss_5"]).reshape(-1)
            reductions = load_array(
                directory, entries["reduction_5"]).reshape(-1)
            self.assertTrue(np.allclose(
                reductions, (baseline - frozen) / baseline,
                rtol=1e-12, atol=1e-14))

    def test_v44_l5_raw_draw_manifest(self):
        facts = m3._l5_build_combination_fixture(101)
        chain_facts, chains = m3._l5_build_chain_fixture(101)
        registry = m3.RNGDomainUseRegistry()
        field_derivation = m3._v44_draw(
            "L5", "permuted", "OBSERVED", 42, 0, 0, registry)
        mapping = field_derivation.accepted_derangement()
        permuted, rows, accuracy = m3._v44_l5_permuted_combo(facts, mapping)
        permuted_chain = [dict(fact) for fact in chain_facts]
        for index, fact in enumerate(permuted_chain):
            fact["content"] = chain_facts[mapping[index]]["content"]
        returned, expected = m3._v44_l5_content_rows(
            m3._L5FactStore(permuted, permuted_chain, chains), chain_facts)
        with tempfile.TemporaryDirectory() as directory:
            writer = RawArtifactWriter(directory)
            chain_derivation = m3._v44_draw(
                "L5", "permuted", "OBSERVED", 42, 0, 1, registry)
            chain_mapping = chain_derivation.accepted_derangement()
            m3._v44_write_l5_draw(
                writer, "OBSERVED", 0,
                [field_derivation.artifact_record(mapping),
                 chain_derivation.artifact_record(chain_mapping)],
                permuted, rows, accuracy, mapping,
                permuted_chain, chain_mapping, returned, expected)
            writer.finalize()
            manifest = validate_manifest(directory, require_full_family=False)
            self.assertEqual(len(manifest["draws"]), 1)
            self.assertEqual(len(returned), 40)

    def test_v44_manifest_detects_nested_descriptor_tamper(self):
        fixture = m3._l1_build_fixture(101)
        sets = m3._l1_build_candidate_sets(101)
        result = m3._v44_l1_arm(fixture["measured_entries"], sets, list(range(200)))
        with tempfile.TemporaryDirectory() as directory:
            writer = RawArtifactWriter(directory)
            registry = m3.RNGDomainUseRegistry()
            draw = m3._v44_draw(
                "L1", "frozen", "OBSERVED", 42, 0, 0, registry)
            accepted = draw.permutation()
            m3._v44_write_l1_draw(
                writer, "L1.frozen", "OBSERVED", 0,
                [draw.artifact_record(accepted)], fixture["measured_entries"],
                sets, result, list(range(200)))
            writer.finalize()
            manifest_path = f"{directory}/m3_v44_raw_manifest.json"
            with open(manifest_path, encoding="utf-8") as handle:
                manifest = m3.json.load(handle)
            manifest["arrays"][0]["shape"] = [999]
            with open(manifest_path, "w", encoding="utf-8") as handle:
                m3.json.dump(manifest, handle, sort_keys=True, separators=(",", ":"))
            with self.assertRaises(ValueError):
                validate_manifest(directory, require_full_family=False)

    def test_v44_manifest_requires_selected_family_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = RawArtifactWriter(
                directory, expected_families=("L1.frozen",))
            writer.finalize()
            with self.assertRaises(ValueError):
                validate_manifest(directory)

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
