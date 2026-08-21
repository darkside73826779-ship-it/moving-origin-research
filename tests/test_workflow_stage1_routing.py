"""Stage-1 routing fixtures and negatives (Regime B, 2026-08-21)."""

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools/workflow_stage1_validator.py"
SPEC = importlib.util.spec_from_file_location("workflow_stage1_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load workflow_stage1_validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
evaluate = VALIDATOR.evaluate
output_digest = VALIDATOR.output_digest
validate_input = VALIDATOR.validate_input


class WorkflowStage1RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / "specs/data/workflow_stage1_validator_contract_v1.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((ROOT / "specs/data/workflow_stage1_routing_fixtures_v1.json").read_text(encoding="utf-8"))

    def test_all_ordered_cases_and_digests(self):
        actual_ids = [case["case_id"] for case in self.fixture["cases"]]
        self.assertEqual(len(actual_ids), len(set(actual_ids)))
        self.assertEqual(set(self.contract["expected_output_sha256"]), set(actual_ids))
        for case in self.fixture["cases"]:
            actual = evaluate(case["input"])
            self.assertEqual(case["expected"], actual, case["case_id"])
            self.assertEqual(self.contract["expected_output_sha256"][case["case_id"]], output_digest(actual), case["case_id"])

    def test_four_schema_negatives(self):
        by_id = {case["case_id"]: case for case in self.fixture["cases"]}
        for negative in self.contract["schema_negative_cases"]:
            value = copy.deepcopy(by_id[negative["base_case_id"]]["input"])
            tokens = [token for token in negative["json_pointer"].split("/") if token][1:]
            target = value
            for token in tokens[:-1]:
                target = target[int(token)] if isinstance(target, list) else target[token]
            final = tokens[-1]
            if negative.get("operation") == "remove":
                if isinstance(target, list):
                    del target[int(final)]
                else:
                    del target[final]
            else:
                if isinstance(target, list):
                    target[int(final)] = negative["replacement"]
                else:
                    target[final] = negative["replacement"]
            with self.assertRaises(ValueError, msg=negative["id"]):
                validate_input(value)


if __name__ == "__main__":
    unittest.main()
