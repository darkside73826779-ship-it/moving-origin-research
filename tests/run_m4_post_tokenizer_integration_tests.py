"""Identity-first, standard-library-only wrapper for the selected M4 tests."""

from __future__ import annotations

import hashlib
import importlib
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path("/workspace") if pathlib.Path("/workspace").is_dir() else pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    ".gitattributes": "03a4a697fd0aefe179874343764ac8fba05ea1f7df2076a1b0ff9b31acb6d994",
    "src/__init__.py": "7bfcb8aa72784807a9d941e2f5784593906f0f216624d5cd736c82339027bdca",
    "src/m4_post_tokenizer_integration.py": "8964de5daf745226771818ab59f2cc75ef29ccbc5d09b43b6dae102b876b2f1b",
    "src/test_m4_post_tokenizer_integration.py": "9878ec7b6c2e8f5c81bd2944e5c811cc1fcdc38a712e4607ce351c6177b18962",
    "specs/data/m4_tokenizer_executable_package_v1.json": "ee5f7bc601d94153d5819453d2f22a8fc6110103c88bd8242ac3ebe5c78ea2bc",
    "specs/data/m4_tokenizer_executable_package_v1.json.sha256": "8237c04033cb77f90ce62fecd2f7adf8866426cdfd95360623f8088b3989903c",
    "specs/data/m4_post_tokenizer_integration_contract_v1.json": "9b562397a7b322e9ac27406d33572815b04eb06978f204ea6d8c5ba13514c778",
    "specs/data/m4_post_tokenizer_integration_contract_v1.json.sha256": "65efd57ee942f78dcb2bdd657a3e8010885fad0f8f9a26012611b1f6d04bae42",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json": "e8b3d13043d6484eebc21791bda7f49a1458a657c8d1590a7447be96f3c99916",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json.sha256": "d1ce2a8ad0ac79741853b80d11bb48e339fc0c8c0e2fbb9a65cee7d393ce60cf",
    "artifacts/m4_tokenizer_materialization/tokenizer_materialization.json": "19a49a9262be81d30866befda3801b2fc97ef23a8d946d3cc1e4b5de189b3158",
    "artifacts/m4_tokenizer_materialization/tokenizer_materialization.json.sha256": "9ca61b765be8558551a70966eda34cba8f8978d8c6c968d62bce0e5977e026b4",
}
EXPECTED_TEST_COUNT = 49


def fail(message: str) -> None:
    raise SystemExit("INSTRUMENT_FAILURE: " + message)


for relative, expected in EXPECTED.items():
    path = ROOT / relative
    if not path.is_file() or path.is_symlink(): fail("path identity " + relative)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected: fail("raw identity " + relative)

LF_BOUND = (
    "specs/data/m4_post_tokenizer_integration_contract_v1.json",
    "specs/data/m4_post_tokenizer_integration_contract_v1.json.sha256",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json.sha256",
    "specs/data/m4_post_tokenizer_combined_integration_inventory_v1.json",
    "specs/data/m4_post_tokenizer_combined_integration_inventory_v1.json.sha256",
    "specs/data/m4_post_tokenizer_integration_oci_launch_contract_v1.json",
    "specs/data/m4_post_tokenizer_integration_oci_launch_contract_v1.json.sha256",
)
for relative in LF_BOUND:
    raw = (ROOT / relative).read_bytes()
    if b"\r" in raw or not raw.endswith(b"\n"): fail("LF identity " + relative)
for relative in LF_BOUND[::2]:
    raw = (ROOT / relative).read_bytes()
    sidecar = (ROOT / (relative + ".sha256")).read_text("ascii").strip().split()
    if len(sidecar) != 2 or sidecar[0] != hashlib.sha256(raw).hexdigest() or sidecar[1] != pathlib.Path(relative).name:
        fail("sidecar identity " + relative)
launch = json.loads((ROOT / LF_BOUND[6]).read_bytes())
inventory_raw = (ROOT / LF_BOUND[4]).read_bytes()
if launch.get("inventory_sha256") != hashlib.sha256(inventory_raw).hexdigest(): fail("launch inventory cascade")
if launch.get("expected_test_count") != EXPECTED_TEST_COUNT: fail("launch test count")
mount = "type=bind,src=${MOR_RELEASED_CHECKOUT},dst=/workspace,readonly"
if launch.get("command_tokens", []).count(mount) != 1: fail("launch mount placeholder")

if (ROOT / "src/__init__.py").stat().st_size == 0: fail("package marker empty")
if str(ROOT) in sys.path: sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))
module = importlib.import_module("src.test_m4_post_tokenizer_integration")
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
if suite.countTestCases() != EXPECTED_TEST_COUNT: fail("test discovery count")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
