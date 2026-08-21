import hashlib
import inspect
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))
import l8_gpu_adoption as subject


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_count_event_polarity():
    passing_beta = [.25] * 5
    passing_rho = [.8] * 5
    assert not subject.complete_false_kill(passing_beta, passing_rho)
    assert subject.complete_false_kill([.25, .19, .25, .25, .25], passing_rho)
    assert subject.complete_false_kill(passing_beta, [.8, None, .8, .8, .8])
    null_false_pass = not subject.complete_false_kill(passing_beta, passing_rho)
    assert null_false_pass


def test_header_topology(monkeypatch):
    fake = SimpleNamespace(__version__="2.13.0+cu130", version=SimpleNamespace(cuda="13.0"),
                           cuda=SimpleNamespace(get_device_name=lambda _: "GPU"))
    monkeypatch.setattr(subject, "torch", fake)
    config = subject.materialize_config("a" * 40)
    header = subject.make_header(config, 3840, 16)
    assert list(header) == ["configuration", "numpy_version", "torch_version",
                            "cuda_runtime_version", "gpu_model", "producer_worker_count",
                            "derived_seed_collision_count"]
    assert list(header["configuration"]) == subject.CONFIG_KEYS


def test_config_self_identity():
    before = subject.CONFIG_TEMPLATE.read_bytes()
    config = subject.materialize_config("b" * 40)
    assert config["implementation_sha"] == "b" * 40
    assert hashlib.sha256(subject.canonical_bytes(config)).hexdigest()
    assert subject.CONFIG_TEMPLATE.read_bytes() == before


def test_deterministic_row_types():
    rows = subject.deterministic_rows()
    assert len(rows) == 11 and all(row["pass"] for row in rows)
    assert [row["family"] for row in rows] == ["rho"] * 7 + ["complete_verdict"] * 4
    assert list(rows[0]) == ["id", "family", "cpu_observed", "gpu_observed",
                             "cpu_predicate", "gpu_predicate", "pass"]


def test_rehearsal_status_enum():
    contract = load("specs/data/l8_gpu_adoption_rehearsal_contract_v1.json")
    allowed = {"INSTRUMENT_FAILURE", "SCHEMA_REJECTED", "PAYLOAD_IDENTICAL",
               "INTERRUPTED_RECOVERED", "STATISTICAL_FAILURE"}
    assert len(contract["rows"]) == 12
    assert {row["expected_status"] for row in contract["rows"]} <= allowed
    assert all(list(row) == ["case_id", "injected_boundary", "expected_status", "case_assertion"]
               for row in contract["rows"])


def test_rehearsal_filesystem(tmp_path):
    contract = load("specs/data/l8_gpu_adoption_rehearsal_contract_v1.json")
    assert contract["preserved_paths"] == [
        "specs/data/l8_gpu_adoption_known_good_v1.json",
        "specs/data/l8_gpu_adoption_known_good_v1.json.sha256",
        "specs/data/l8_gpu_adoption_rehearsal_prior_v1.json",
        "specs/data/l8_gpu_adoption_rehearsal_prior_v1.json.sha256"]
    case = tmp_path / "01-cuda_unavailable"
    case.mkdir()
    for name in ("result.json", "result.json.sha256"):
        (case / name).write_bytes(b"x")
    assert sorted(path.name for path in case.iterdir()) == ["result.json", "result.json.sha256"]


def test_repeat_custody_protocol():
    source = inspect.getsource(subject.two_child_custody)
    assert "range(2)" in source
    assert source.count("recv_bytes()") == 3
    assert "PAYLOAD_REPEAT_MISMATCH" in source
    child_source = inspect.getsource(subject._child_sentinel)
    assert child_source.count("send_bytes") == 2


def test_fullscreen_pipeline_contract():
    import l8_g2g4_minimal_full_screen as cpu_full
    assert cpu_full.N_SIMS == 2000 and cpu_full.N_WORKERS == 16
    assert len(cpu_full.geometry_order()) == 20 and len(cpu_full.cells()) == 240
    assert subject.FULLSCREEN_WORKERS == 16 and subject.FULLSCREEN_QUEUE_DEPTH == 2
    assert hasattr(subject, "run_fullscreen_gpu")


def test_counter_invariants():
    attempted, valid, invalid = 256, 255, 1
    assert valid + invalid == attempted and valid > 0
    assert subject.summarize_arm


def test_dependency_freeze():
    manifest = load("specs/data/l8_gpu_adoption_dependencies_v1.json")
    assert manifest["python"] == {"implementation": "CPython", "version": "3.11.9"}
    for item in manifest["packages"]:
        raw = json.dumps({"url": item["url"].split("#", 1)[0],
                          "archive_info": {"hash": "sha256=" + item["sha256"]}})
        subject.validate_direct_url_record(item, item["version"], raw)
        with pytest.raises(ValueError):
            subject.validate_direct_url_record(item, "wrong", raw)


def test_rng_identity():
    assert subject.pa.combo_seed(0.0, .5, .5, .01) == subject.pa.combo_seed(0.0, .5, .5, .01)
    config = subject.materialize_config("c" * 40)
    assert config["rng"]["identity_fields"] == ["cell_ordinal", "arm_ordinal",
                                                  "repetition_index", "seed_index"]
    assert subject.collision_count(config) == 3840


def test_coverage_tie_rule():
    fixtures = load("specs/data/l8_gpu_adoption_tie_fixtures_v1.json")["fixtures"]
    for fixture in fixtures:
        indices = subject.coverage_indices(np.array(fixture["c_prime"]), fixture["c_min"], fixture["tau"])
        assert indices.tolist() == fixture["expected_coverage_indices"]
        correct = np.asarray(fixture["correct"])
        selected_correct = correct[indices]
        assert selected_correct.tolist() == fixture["expected_answered_correctness"]
        risk = float(np.count_nonzero(~selected_correct) / selected_correct.size)
        assert risk == fixture["expected_risk"]
        d_seed = np.asarray(fixture["d_seed"], dtype=np.float64)
        old_nw = subject.pa.N_W
        subject.pa.N_W = 4
        try:
            beta, failed = subject.pa.beta_star_for_seed(d_seed)
        finally:
            subject.pa.N_W = old_nw
        assert not failed and abs(beta - fixture["expected_beta_star"]) <= 1e-12
        assert abs(subject.rho_from_means(d_seed.mean(axis=1)) - fixture["expected_rho"]) <= 1e-12
    swapped = np.asarray(fixtures[1]["correct"])[[1, 0, 2, 3]]
    chosen = subject.coverage_indices(np.asarray(fixtures[1]["c_prime"]), .25, .999999)
    assert bool(swapped[chosen][0]) is True  # mutation cannot satisfy the committed false answer.


def test_queue_residency_bound():
    assert subject.FULLSCREEN_QUEUE_DEPTH == 2
    source = inspect.getsource(subject._full_arm)
    assert "maxsize=FULLSCREEN_QUEUE_DEPTH" in source
    assert "FULLSCREEN_WORKERS" in source


def test_locked_bar_literals():
    fixture = load("specs/data/l8_gpu_adoption_tie_fixtures_v1.json")
    assert subject.BETA_BAR == fixture["constants"]["beta_bar"] == .2
    assert subject.RHO_BAR == fixture["constants"]["rho_bar"] == .8
    assert subject.pa.N_SEEDS == 5


def test_unknown_field_rejection():
    with pytest.raises(ValueError):
        subject.strict_json_bytes(b'{"a":1,"a":2}')
    config = subject.materialize_config("d" * 40)
    config["unknown"] = 1
    with pytest.raises(ValueError):
        subject.validate_config(config)
    with pytest.raises(ValueError):
        subject.strict_json_bytes(b'{"x":NaN}')


def test_atomic_pair_recovery(tmp_path):
    target = tmp_path / "result.json"
    prior = b'{"prior":true}'
    target.write_bytes(prior)
    target.with_name("result.json.sha256").write_bytes(
        f"{hashlib.sha256(prior).hexdigest()}  result.json\n".encode("ascii"))
    with pytest.raises(subject.ContractFailure) as failure:
        subject.atomic_pair(target, b'{"new":true}', interrupt=True)
    assert failure.value.failure["message_code"] == "PUBLICATION_INTERRUPTED"
    assert target.read_bytes() == prior
    assert (tmp_path / "result.json.tmp.incomplete").is_file()
    assert not (tmp_path / "result.json.sha256.tmp.incomplete").exists()


def test_authorization_boundary():
    approval = (ROOT / "handoffs/REBECCA_L8_GPU_V1.5_APPROVAL_AND_RELEASE_2026-08-21.md").read_text()
    assert "including the B11 comparator operationalization" in approval
    assert "two permitted executions" in approval
    public = [name for name in dir(subject) if not name.startswith("_")]
    assert not any("scor" in name.lower() or "protected_seed" in name.lower() for name in public)


def test_primitive_tape_reproduces_baseline_and_gpu():
    if subject.torch is None or not subject.torch.cuda.is_available():
        pytest.skip("required CUDA runtime unavailable")
    task = (0, 0, 0, 1, 10, 4, 0.0, 0.5, 0.5, 0.01, 1.0)
    tape = subject.make_tape(task)
    cpu = subject.evaluate_tape_cpu(tape)
    old_w, old_nw = subject.pa.W, subject.pa.N_W
    subject.pa.W, subject.pa.N_W = 10, 4
    try:
        seed = subject.pa.combo_seed(0.0, 0.5, 0.5, 0.01)
        baseline = subject.pa.simulate_one_seed(np.random.default_rng(seed), 0.0, 0.5, 1.0, 0.5, 0.01)
    finally:
        subject.pa.W, subject.pa.N_W = old_w, old_nw
    assert np.array_equal(cpu["d_seed"][0, 0], baseline)
    gpu = subject.evaluate_tape_gpu(tape)
    comparison = subject.compare_block(cpu, gpu)
    assert comparison["masks_equal"] and comparison["rho_masks_equal"]
    assert comparison["predicates_equal"]
    assert comparison["max_beta_delta"] <= 1e-12
    assert comparison["max_rho_delta"] <= 1e-12
