"""Identity-first, standard-library-only wrapper for the selected M4 tests."""

from __future__ import annotations

import hashlib
import importlib
import pathlib
import sys
import unittest

ROOT = pathlib.Path("/workspace") if pathlib.Path("/workspace").is_dir() else pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    ".gitattributes": "52228481c5f216876d9152f927b8f4356038b0d30e1c95bac97f16adaf48aaea",
    "src/__init__.py": "7bfcb8aa72784807a9d941e2f5784593906f0f216624d5cd736c82339027bdca",
    "src/m4_post_tokenizer_integration.py": "932905d33ec37c3f0da8be4cd76824d347dbe16b58825f30bac280a06505552b",
    "src/test_m4_post_tokenizer_integration.py": "934fa8a8de11ab26a8ab43a6f90d8c9babd8a025975df01db96f47f924a354dc",
    "specs/data/m4_tokenizer_executable_package_v1.json": "2c6b13405d79cc105ec1ef8dae913781867108175c36ddb863b6ea7ccd915610",
    "specs/data/m4_tokenizer_executable_package_v1.json.sha256": "a95febab7cd0031ebc74c05678de84cb6ed6329e8bd3810cf7ddf18d57b107fb",
    "specs/data/m4_post_tokenizer_integration_contract_v1.json": "9b562397a7b322e9ac27406d33572815b04eb06978f204ea6d8c5ba13514c778",
    "specs/data/m4_post_tokenizer_integration_contract_v1.json.sha256": "65efd57ee942f78dcb2bdd657a3e8010885fad0f8f9a26012611b1f6d04bae42",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json": "e8b3d13043d6484eebc21791bda7f49a1458a657c8d1590a7447be96f3c99916",
    "specs/data/m4_post_tokenizer_synthetic_integration_fixture_v1.json.sha256": "d1ce2a8ad0ac79741853b80d11bb48e339fc0c8c0e2fbb9a65cee7d393ce60cf",
    "artifacts/m4_tokenizer_materialization/tokenizer_materialization.json": "19a49a9262be81d30866befda3801b2fc97ef23a8d946d3cc1e4b5de189b3158",
    "artifacts/m4_tokenizer_materialization/tokenizer_materialization.json.sha256": "9ca61b765be8558551a70966eda34cba8f8978d8c6c968d62bce0e5977e026b4",
}
EXPECTED_TEST_COUNT = 32


def fail(message: str) -> None:
    raise SystemExit("INSTRUMENT_FAILURE: " + message)


for relative, expected in EXPECTED.items():
    path = ROOT / relative
    if not path.is_file() or path.is_symlink(): fail("path identity " + relative)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected: fail("raw identity " + relative)

if (ROOT / "src/__init__.py").stat().st_size == 0: fail("package marker empty")
if str(ROOT) in sys.path: sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))
module = importlib.import_module("src.test_m4_post_tokenizer_integration")
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
if suite.countTestCases() != EXPECTED_TEST_COUNT: fail("test discovery count")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
