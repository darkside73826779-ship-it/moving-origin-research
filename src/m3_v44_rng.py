"""Frozen M3 V4.4 SHA-256 counter-mode control RNG.

This module implements only the RNG and statistical utility contracts in
``m3_v4_4_implementation_contract_amendment.md`` Contracts 1, 3, 4, and 6.
It is deliberately independent of the candidate laws, control transforms,
and diagnostic harness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import math
import struct
import unicodedata
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np


PROTOCOL_ID = "M3-V4.4-SHA256-CTR-FY-v1"
ROOT_DOMAIN = b"MOVING-ORIGIN/M3/V4.4/CONTROL-RNG/v1"
UINT64_MODULUS = 1 << 64
LOW_53_MASK = (1 << 53) - 1
MANTISSA_DENOMINATOR = 1 << 53
INNOVATION_SHAPE = (1110, 8)
INNOVATION_VARIANCE = 0.05
NULL_REPLICATE_COUNT = 1000
ORDER_STATISTIC_985_ONE_INDEXED = 985


@dataclass(frozen=True)
class SubdrawDefinition:
    """One allowed component of a frozen stochastic family."""

    component: str
    kind: str
    size: int
    accepted_permutation: bool


def _subdraws(
    component: str, kind: str, size: int, accepted_permutation: bool
) -> Dict[int, SubdrawDefinition]:
    return {
        0: SubdrawDefinition(
            component=component,
            kind=kind,
            size=size,
            accepted_permutation=accepted_permutation,
        )
    }


# Contract 3's complete, role-specific subdraw registry.  The key components
# use the exact protocol role strings.
SUBDRAW_REGISTRY: Dict[Tuple[str, str, str], Dict[int, SubdrawDefinition]] = {
    **{
        ("L1", arm, role): _subdraws(component, "fisher_yates", size, True)
        for arm, component, size in (
            ("frozen", "tie-break reassignment permutation", 200),
            ("fair_naive", "identifier permutation", 200),
            ("permuted", "(age,rehearsal)-to-entry mapping permutation", 200),
            ("shuffled", "priming query reassignment", 1200),
        )
        for role in ("OBSERVED", "NULL")
    },
    **{
        ("L3", arm, role): _subdraws(
            "Gaussian innovations", "box_muller_gaussian", 8880, False
        )
        for arm in ("frozen", "oracle")
        for role in ("OBSERVED", "NULL")
    },
    ("L3", "permuted", "OBSERVED"): {
        0: SubdrawDefinition(
            "Gaussian innovations", "box_muller_gaussian", 8880, False
        ),
        1: SubdrawDefinition(
            "channel derangement", "derangement", 8, True
        ),
    },
    ("L3", "permuted", "NULL"): {
        0: SubdrawDefinition(
            "channel derangement", "derangement", 8, True
        ),
    },
    ("L3", "shuffled", "OBSERVED"): {
        0: SubdrawDefinition(
            "Gaussian innovations", "box_muller_gaussian", 8880, False
        ),
        1: SubdrawDefinition(
            "cycle-order permutation", "fisher_yates", 1010, True
        ),
    },
    ("L3", "shuffled", "NULL"): {
        0: SubdrawDefinition(
            "cycle-order permutation", "fisher_yates", 1010, True
        ),
    },
    **{
        ("L5", "permuted", role): {
            0: SubdrawDefinition(
                "field derangement (acquired_at/validity)",
                "derangement",
                200,
                True,
            ),
            1: SubdrawDefinition(
                "chain content derangement", "derangement", 200, True
            ),
        }
        for role in ("OBSERVED", "NULL")
    },
}


def _require_uint(name: str, value: int, bits: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an unsigned {bits}-bit integer")
    if not 0 <= value < (1 << bits):
        raise ValueError(f"{name} is outside unsigned {bits}-bit range")


def _require_text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str")
    return unicodedata.normalize("NFC", value)


def encode_domain_text(value: str) -> bytes:
    """Return C6's NFC UTF-8 text encoding with a u16be byte length."""

    encoded = _require_text("domain text", value).encode("utf-8")
    if len(encoded) > 0xFFFF:
        raise ValueError("domain text exceeds the u16 byte-length encoding")
    return struct.pack(">H", len(encoded)) + encoded


def derive_stream_key(
    law: str,
    arm: str,
    draw_role: str,
    scoring_seed: int,
    replicate_index: int,
    subdraw_index: int,
) -> bytes:
    """Derive the exact 32-byte SHA-256 key specified by V4.4 §6."""

    law = _require_text("law", law)
    arm = _require_text("arm", arm)
    draw_role = _require_text("draw_role", draw_role)
    if draw_role not in ("OBSERVED", "NULL"):
        raise ValueError("draw_role must be OBSERVED or NULL")
    _require_uint("scoring_seed", scoring_seed, 64)
    _require_uint("replicate_index", replicate_index, 32)
    _require_uint("subdraw_index", subdraw_index, 32)
    key_material = b"".join(
        (
            ROOT_DOMAIN,
            b"\x00",
            encode_domain_text(law),
            encode_domain_text(arm),
            encode_domain_text(draw_role),
            struct.pack(">Q", scoring_seed),
            struct.pack(">I", replicate_index),
            struct.pack(">I", subdraw_index),
        )
    )
    return hashlib.sha256(key_material).digest()


def subdraw_definition(
    law: str, arm: str, draw_role: str, subdraw_index: int
) -> SubdrawDefinition:
    """Return the Contract 3 entry, failing closed for an unregistered tuple."""

    key = (_require_text("law", law), _require_text("arm", arm),
           _require_text("draw_role", draw_role))
    _require_uint("subdraw_index", subdraw_index, 32)
    try:
        return SUBDRAW_REGISTRY[key][subdraw_index]
    except KeyError as exc:
        raise ValueError(
            "unregistered V4.4 subdraw: "
            f"(law={key[0]!r}, arm={key[1]!r}, role={key[2]!r}, "
            f"subdraw={subdraw_index})"
        ) from exc


class SHA256CounterStream:
    """Sequential uint64be words from SHA256(key || u64be(counter))."""

    def __init__(self, key: bytes):
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("key must be exactly 32 bytes")
        self.key = key
        self._counter = 0
        self._block = b""
        self._offset = 0
        self.block_count = 0
        self.word_count = 0
        self.rejection_count = 0
        self._consumed_digest = hashlib.sha256()

    def _next_block(self) -> None:
        if self._counter >= UINT64_MODULUS:
            raise OverflowError("SHA-256 counter exhausted")
        self._block = hashlib.sha256(
            self.key + struct.pack(">Q", self._counter)
        ).digest()
        self._counter += 1
        self._offset = 0
        self.block_count += 1

    def next_word(self) -> int:
        """Consume and return the next non-overlapping unsigned uint64be word."""

        if self._offset == len(self._block):
            self._next_block()
        word_bytes = self._block[self._offset:self._offset + 8]
        self._offset += 8
        if len(word_bytes) != 8:
            raise AssertionError("counter block split a uint64 word")
        self.word_count += 1
        self._consumed_digest.update(word_bytes)
        return struct.unpack(">Q", word_bytes)[0]

    @property
    def sha256_digest(self) -> str:
        """SHA-256 hex digest of raw bytes actually consumed as words."""

        return self._consumed_digest.hexdigest()


class RNGDomainUseRegistry:
    """Optional in-process guard against reusing a protocol domain tuple.

    The protocol's no-reuse rule is a run-level custody rule.  Callers that
    construct many draws can pass one shared registry to ``RNGDerivation``.
    It is deliberately opt-in so independent JUDGE recomputation is possible.
    """

    def __init__(self) -> None:
        self._used = set()

    def claim(self, domain: Tuple[str, str, str, int, int, int]) -> None:
        if domain in self._used:
            raise ValueError(f"V4.4 RNG domain reused: {domain!r}")
        self._used.add(domain)


def randbelow(stream: SHA256CounterStream, modulus: int) -> int:
    """Uniformly sample ``[0, modulus)`` using Contract 6's exact rejection."""

    _require_uint("modulus", modulus, 64)
    if modulus == 0:
        raise ValueError("modulus must be positive")
    limit = (UINT64_MODULUS // modulus) * modulus
    while True:
        word = stream.next_word()
        if word < limit:
            return word % modulus
        stream.rejection_count += 1


def fisher_yates_permutation(stream: SHA256CounterStream, size: int) -> List[int]:
    """Return the Contract 6 Fisher--Yates permutation of ``range(size)``."""

    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError("size must be an integer")
    if size < 0:
        raise ValueError("size must be non-negative")
    result = list(range(size))
    for index in range(size - 1, 0, -1):
        partner = randbelow(stream, index + 1)
        result[index], result[partner] = result[partner], result[index]
    return result


def derangement(stream: SHA256CounterStream, size: int) -> List[int]:
    """Draw consecutive full FY permutations until one has no fixed point."""

    if size < 2:
        raise ValueError("a derangement requires size >= 2")
    while True:
        candidate = fisher_yates_permutation(stream, size)
        if all(index != value for index, value in enumerate(candidate)):
            return candidate


def _word_record(word: int) -> Dict[str, Any]:
    return {
        "word_hex": f"{word:016x}",
        "mantissa_low53": word & LOW_53_MASK,
    }


def box_muller_pair(stream: SHA256CounterStream) -> Tuple[float, float]:
    """Consume one Contract 1.3 Box--Muller pair from ``stream``.

    A zero low-53-bit first uniform is rejected, but a zero second uniform is
    valid.  This function is intentionally small and public to make the
    forced-rejection conformance case directly testable.
    """

    while True:
        first_word = stream.next_word()
        first_mantissa = first_word & LOW_53_MASK
        if first_mantissa:
            break
        stream.rejection_count += 1
    second_word = stream.next_word()
    first_uniform = first_mantissa / MANTISSA_DENOMINATOR
    second_uniform = (second_word & LOW_53_MASK) / MANTISSA_DENOMINATOR
    radius = math.sqrt(-2.0 * math.log(first_uniform))
    angle = 2.0 * math.pi * second_uniform
    return radius * math.cos(angle), radius * math.sin(angle)


def gaussian_innovation_array(
    stream: SHA256CounterStream,
    *,
    emit_conformance_vectors: bool = True,
) -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
    """Generate Contract 1's 1110x8 scaled innovation array.

    Values are filled flat C row-major (time-major, then channel) order and
    are scaled once by ``sqrt(0.05)``.  The returned conformance structure is
    JSON-serializable and belongs in the associated RNG derivation record.
    """

    scale = math.sqrt(INNOVATION_VARIANCE)
    values = np.empty(INNOVATION_SHAPE[0] * INNOVATION_SHAPE[1],
                      dtype=np.float64)
    first_twenty_words: List[Dict[str, Any]] = []
    first_ten_pairs: List[Dict[str, Any]] = []

    def next_word_with_vector_capture() -> int:
        word = stream.next_word()
        if len(first_twenty_words) < 20:
            first_twenty_words.append(_word_record(word))
        return word

    pair_count = values.size // 2
    for pair_index in range(pair_count):
        first_attempts: List[Dict[str, Any]] = []
        while True:
            first_word = next_word_with_vector_capture()
            first_record = _word_record(first_word)
            first_attempts.append(first_record)
            first_mantissa = first_word & LOW_53_MASK
            if first_mantissa:
                break
            stream.rejection_count += 1
        second_word = next_word_with_vector_capture()
        second_mantissa = second_word & LOW_53_MASK
        u1 = first_mantissa / MANTISSA_DENOMINATOR
        u2 = second_mantissa / MANTISSA_DENOMINATOR
        radius = math.sqrt(-2.0 * math.log(u1))
        angle = 2.0 * math.pi * u2
        z1 = radius * math.cos(angle)
        z2 = radius * math.sin(angle)
        values[2 * pair_index] = scale * z1
        values[2 * pair_index + 1] = scale * z2
        if pair_index < 10:
            first_ten_pairs.append(
                {
                    "pair_index": pair_index,
                    "u1_words": first_attempts,
                    "u1_mantissa": first_mantissa,
                    "u2_word": _word_record(second_word),
                    "u2_mantissa": second_mantissa,
                    "u1": u1,
                    "u2": u2,
                    "z1": z1,
                    "z2": z2,
                    "scaled_epsilon": [values[2 * pair_index],
                                       values[2 * pair_index + 1]],
                }
            )

    innovations = values.reshape(INNOVATION_SHAPE)
    if not np.all(np.isfinite(innovations)):
        raise FloatingPointError("non-finite Gaussian innovation generated")
    if not emit_conformance_vectors:
        return innovations, None
    little_endian_bytes = innovations.astype("<f8", copy=False).tobytes(order="C")
    vectors = {
        "vector_a": {
            "first_20_consumed_stream_words": first_twenty_words,
            "first_10_pairs": first_ten_pairs,
        },
        "vector_b": {
            "encoding": "C-row-major little-endian binary64",
            "epsilon_sha256": hashlib.sha256(little_endian_bytes).hexdigest(),
        },
    }
    return innovations, vectors


@dataclass
class RNGDerivation:
    """One fully named frozen protocol stream plus its artifact record."""

    law: str
    arm: str
    draw_role: str
    scoring_seed: int
    replicate_index: int
    subdraw_index: int
    use_registry: Optional[RNGDomainUseRegistry] = None
    _stream: SHA256CounterStream = field(init=False, repr=False)
    _key: bytes = field(init=False, repr=False)
    _conformance_vectors: Optional[Dict[str, Any]] = field(
        init=False, default=None, repr=False
    )

    def __post_init__(self) -> None:
        self.law = _require_text("law", self.law)
        self.arm = _require_text("arm", self.arm)
        self.draw_role = _require_text("draw_role", self.draw_role)
        # This validates the role-specific Contract 3 registry before a stream
        # can be consumed.
        subdraw_definition(
            self.law, self.arm, self.draw_role, self.subdraw_index
        )
        self._key = derive_stream_key(
            self.law,
            self.arm,
            self.draw_role,
            self.scoring_seed,
            self.replicate_index,
            self.subdraw_index,
        )
        if self.use_registry is None:
            raise ValueError(
                'a run-level RNGDomainUseRegistry is required for every '
                'production V4.4 derivation')
        self.use_registry.claim(
            (
                self.law,
                self.arm,
                self.draw_role,
                self.scoring_seed,
                self.replicate_index,
                self.subdraw_index,
            )
        )
        self._stream = SHA256CounterStream(self._key)

    @property
    def stream(self) -> SHA256CounterStream:
        return self._stream

    @property
    def stream_key_hex(self) -> str:
        return self._key.hex()

    def permutation(self) -> List[int]:
        """Generate the registered Fisher--Yates component."""

        definition = subdraw_definition(
            self.law, self.arm, self.draw_role, self.subdraw_index
        )
        if definition.kind != "fisher_yates":
            raise ValueError("this registered subdraw is not a permutation")
        return fisher_yates_permutation(self.stream, definition.size)

    def accepted_derangement(self) -> List[int]:
        """Generate the registered accepted derangement component."""

        definition = subdraw_definition(
            self.law, self.arm, self.draw_role, self.subdraw_index
        )
        if definition.kind != "derangement":
            raise ValueError("this registered subdraw is not a derangement")
        return derangement(self.stream, definition.size)

    def gaussian_innovations(self) -> np.ndarray:
        """Generate the registered Gaussian innovation component."""

        definition = subdraw_definition(
            self.law, self.arm, self.draw_role, self.subdraw_index
        )
        if definition.kind != "box_muller_gaussian":
            raise ValueError("this registered subdraw is not Gaussian")
        innovations, vectors = gaussian_innovation_array(self.stream)
        self._conformance_vectors = vectors
        return innovations

    def artifact_record(
        self, accepted_permutation: Optional[Sequence[int]] = None
    ) -> Dict[str, Any]:
        """Emit Contract 4's common record plus Gaussian vectors when present."""

        definition = subdraw_definition(
            self.law, self.arm, self.draw_role, self.subdraw_index
        )
        if definition.accepted_permutation:
            if accepted_permutation is None:
                raise ValueError("this subdraw requires its accepted permutation")
            accepted = list(accepted_permutation)
            if len(accepted) != definition.size:
                raise ValueError(
                    f"accepted permutation must contain {definition.size} values"
                )
            if sorted(accepted) != list(range(definition.size)):
                raise ValueError("accepted permutation is not a permutation")
            if (definition.kind == "derangement"
                    and any(index == value for index, value in enumerate(accepted))):
                raise ValueError("accepted derangement contains a fixed point")
        else:
            if accepted_permutation is not None:
                raise ValueError(
                    "Gaussian-only subdraws require accepted_permutation=None"
                )
            accepted = None
        record: Dict[str, Any] = {
            "rng_protocol_id": PROTOCOL_ID,
            "hash": "SHA-256",
            "root_domain_hex": ROOT_DOMAIN.hex(),
            "law": self.law,
            "arm": self.arm,
            "draw_role": self.draw_role,
            "scoring_seed": self.scoring_seed,
            "replicate_index": self.replicate_index,
            "subdraw_index": self.subdraw_index,
            "stream_key_hex": self.stream_key_hex,
            "derived_key_hex": self.stream_key_hex,
            "stream_block_count": self.stream.block_count,
            "stream_word_count": self.stream.word_count,
            "rejection_count": self.stream.rejection_count,
            "accepted_permutation": accepted,
            "sha256_digest": self.stream.sha256_digest,
        }
        if self._conformance_vectors is not None:
            record["conformance_vectors"] = self._conformance_vectors
        return record


def plus_one_upper_tail_pvalue(
    observed_statistic: float, null_statistics: Iterable[float]
) -> Tuple[float, int]:
    """Return the exact plus-one upper-tail p-value and exceed/tie count."""

    null_values = list(null_statistics)
    if not null_values:
        raise ValueError("at least one null statistic is required")
    all_values = [observed_statistic] + null_values
    if not all(math.isfinite(float(value)) for value in all_values):
        raise ValueError("statistics must all be finite")
    exceed_or_tie_count = sum(
        1 for value in null_values if value >= observed_statistic
    )
    return (
        (1 + exceed_or_tie_count) / (1 + len(null_values)),
        exceed_or_tie_count,
    )


def sorted_null_order_statistic_985(null_statistics: Sequence[float]) -> float:
    """Return V4.4's sorted-null 985th statistic (one-indexed, no interpolation)."""

    if len(null_statistics) != NULL_REPLICATE_COUNT:
        raise ValueError("the V4.4 order statistic requires exactly 1000 nulls")
    if not all(math.isfinite(float(value)) for value in null_statistics):
        raise ValueError("null statistics must all be finite")
    return sorted(null_statistics)[ORDER_STATISTIC_985_ONE_INDEXED - 1]
