"""Focused contract tests for the isolated M3 V4.4 RNG implementation."""

import hashlib
import math
import struct
import unittest

import numpy as np

from m3_v44_rng import (
    INNOVATION_SHAPE,
    LOW_53_MASK,
    ROOT_DOMAIN,
    RNGDerivation,
    RNGDomainUseRegistry,
    SHA256CounterStream,
    box_muller_pair,
    derangement,
    derive_stream_key,
    encode_domain_text,
    fisher_yates_permutation,
    plus_one_upper_tail_pvalue,
    randbelow,
    sorted_null_order_statistic_985,
    subdraw_definition,
)


class WordSequence:
    """Minimal stream substitute for exact rejection/cursor tests."""

    def __init__(self, words):
        self._words = iter(words)
        self.word_count = 0
        self.rejection_count = 0

    def next_word(self):
        self.word_count += 1
        return next(self._words)


class TestM3V44RNG(unittest.TestCase):
    def test_key_uses_exact_binary_encoding_and_nfc(self):
        key = derive_stream_key("L3", "frozen", "OBSERVED", 7, 0, 0)
        material = b"".join(
            (
                ROOT_DOMAIN,
                b"\x00",
                struct.pack(">H", 2) + b"L3",
                struct.pack(">H", 6) + b"frozen",
                struct.pack(">H", 8) + b"OBSERVED",
                struct.pack(">QII", 7, 0, 0),
            )
        )
        self.assertEqual(key, hashlib.sha256(material).digest())
        self.assertEqual(
            encode_domain_text("e\u0301"), encode_domain_text("\u00e9")
        )

    def test_counter_words_are_big_endian_and_accounted_by_block(self):
        key = bytes(range(32))
        stream = SHA256CounterStream(key)
        expected_block_zero = hashlib.sha256(key + struct.pack(">Q", 0)).digest()
        expected_block_one = hashlib.sha256(key + struct.pack(">Q", 1)).digest()
        words = [stream.next_word() for _ in range(5)]
        self.assertEqual(words[0], struct.unpack(">Q", expected_block_zero[:8])[0])
        self.assertEqual(words[3], struct.unpack(">Q", expected_block_zero[24:])[0])
        self.assertEqual(words[4], struct.unpack(">Q", expected_block_one[:8])[0])
        self.assertEqual(stream.word_count, 5)
        self.assertEqual(stream.block_count, 2)
        self.assertEqual(
            stream.sha256_digest,
            hashlib.sha256(expected_block_zero + expected_block_one[:8]).hexdigest(),
        )

    def test_randbelow_rejects_at_or_above_exact_limit(self):
        modulus = 3
        limit = ((1 << 64) // modulus) * modulus
        stream = WordSequence([limit, 7])
        self.assertEqual(randbelow(stream, modulus), 1)
        self.assertEqual(stream.word_count, 2)
        self.assertEqual(stream.rejection_count, 1)

    def test_fisher_yates_and_derangement_use_consecutive_words(self):
        permutation = fisher_yates_permutation(WordSequence([0, 1, 0]), 4)
        self.assertEqual(permutation, [2, 3, 1, 0])
        # First n=2 permutation is the identity; the second is accepted.
        stream = WordSequence([1, 0])
        self.assertEqual(derangement(stream, 2), [1, 0])
        self.assertEqual(stream.word_count, 2)
        self.assertEqual(stream.rejection_count, 0)

    def test_box_muller_forced_u1_rejection_advances_cursor(self):
        stream = WordSequence([0, 1, 1 << 52])
        z1, z2 = box_muller_pair(stream)
        radius = math.sqrt(-2.0 * math.log(1.0 / (1 << 53)))
        self.assertAlmostEqual(z1, -radius, places=13)
        self.assertAlmostEqual(z2, 0.0, places=13)
        self.assertEqual(stream.word_count, 3)
        self.assertEqual(stream.rejection_count, 1)
        # A zero u2 is valid and must not be rejected or adjusted.
        zero_u2_stream = WordSequence([1, 0])
        z1, z2 = box_muller_pair(zero_u2_stream)
        self.assertAlmostEqual(z1, radius, places=13)
        self.assertEqual(z2, 0.0)
        self.assertEqual(zero_u2_stream.word_count, 2)
        self.assertEqual(zero_u2_stream.rejection_count, 0)

    def test_gaussian_array_and_common_artifact_record(self):
        derivation = RNGDerivation(
            "L3", "frozen", "OBSERVED", 42, 0, 0, RNGDomainUseRegistry())
        innovations = derivation.gaussian_innovations()
        record = derivation.artifact_record()
        self.assertEqual(innovations.shape, INNOVATION_SHAPE)
        self.assertEqual(innovations.dtype, np.dtype("float64"))
        self.assertTrue(np.all(np.isfinite(innovations)))
        self.assertEqual(record["stream_word_count"], 8880)
        self.assertEqual(record["stream_block_count"], 2220)
        self.assertEqual(record["rejection_count"], 0)
        self.assertIsNone(record["accepted_permutation"])
        self.assertEqual(record["rng_protocol_id"], "M3-V4.4-SHA256-CTR-FY-v1")
        self.assertEqual(record["derived_key_hex"], record["stream_key_hex"])
        vectors = record["conformance_vectors"]
        self.assertEqual(len(vectors["vector_a"]["first_20_consumed_stream_words"]), 20)
        self.assertEqual(len(vectors["vector_a"]["first_10_pairs"]), 10)
        expected_digest = hashlib.sha256(
            innovations.astype("<f8", copy=False).tobytes(order="C")
        ).hexdigest()
        self.assertEqual(vectors["vector_b"]["epsilon_sha256"], expected_digest)
        first_pair = vectors["vector_a"]["first_10_pairs"][0]
        self.assertEqual(
            first_pair["u1_mantissa"],
            int(first_pair["u1_words"][-1]["word_hex"], 16) & LOW_53_MASK,
        )

    def test_registry_and_use_guard_fail_closed(self):
        self.assertEqual(
            subdraw_definition("L3", "permuted", "NULL", 0).kind,
            "derangement",
        )
        with self.assertRaises(ValueError):
            subdraw_definition("L3", "permuted", "NULL", 1)
        domains = RNGDomainUseRegistry()
        RNGDerivation("L1", "frozen", "OBSERVED", 8, 0, 0, domains)
        with self.assertRaises(ValueError):
            RNGDerivation("L1", "frozen", "OBSERVED", 8, 0, 0, domains)
        with self.assertRaises(ValueError):
            RNGDerivation("L1", "frozen", "OBSERVED", 9, 0, 0)

    def test_complete_v44_subdraw_domains_cover_all_nine_families(self):
        expected = {
            ("L1", "frozen", "OBSERVED", 0, "fisher_yates"),
            ("L1", "fair_naive", "NULL", 0, "fisher_yates"),
            ("L1", "permuted", "OBSERVED", 0, "fisher_yates"),
            ("L1", "shuffled", "NULL", 0, "fisher_yates"),
            ("L3", "frozen", "NULL", 0, "box_muller_gaussian"),
            ("L3", "oracle", "OBSERVED", 0, "box_muller_gaussian"),
            ("L3", "permuted", "OBSERVED", 1, "derangement"),
            ("L3", "permuted", "NULL", 0, "derangement"),
            ("L3", "shuffled", "OBSERVED", 1, "fisher_yates"),
            ("L3", "shuffled", "NULL", 0, "fisher_yates"),
            ("L5", "permuted", "OBSERVED", 1, "derangement"),
            ("L5", "permuted", "NULL", 0, "derangement"),
        }
        for law, arm, role, subdraw, kind in expected:
            self.assertEqual(
                subdraw_definition(law, arm, role, subdraw).kind, kind)

    def test_permutation_record_and_plus_one_statistics(self):
        derivation = RNGDerivation(
            "L3", "shuffled", "NULL", 19, 999, 0, RNGDomainUseRegistry())
        accepted = derivation.permutation()
        record = derivation.artifact_record(accepted)
        self.assertEqual(len(accepted), 1010)
        self.assertEqual(sorted(accepted), list(range(1010)))
        self.assertEqual(record["accepted_permutation"], accepted)
        p_value, count = plus_one_upper_tail_pvalue(985.0, list(range(1000)))
        self.assertEqual(count, 15)
        self.assertEqual(p_value, 16 / 1001)
        self.assertEqual(
            sorted_null_order_statistic_985(list(range(1000))), 984
        )


if __name__ == "__main__":
    unittest.main()
