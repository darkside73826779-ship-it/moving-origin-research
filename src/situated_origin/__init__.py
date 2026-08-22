"""Situated-origin runtime for the final project assembly alpha.

The package owns cognitive time and provenance.  Evaluators and model backends
consume its immutable projections; they do not maintain competing histories.
"""

from .contracts import (
    ClaimReceipt,
    CommittedOriginEvent,
    EnvironmentFrame,
    GroundedMemory,
    MemoryQuery,
    OriginDistance,
    OriginEventProposal,
    OriginStamp,
    ProvenanceHandle,
    RecallBundle,
    SituatedContextPacket,
    SituatedOriginFrame,
    Unavailable,
)

__all__ = [
    "ClaimReceipt",
    "CommittedOriginEvent",
    "EnvironmentFrame",
    "GroundedMemory",
    "MemoryQuery",
    "OriginDistance",
    "OriginEventProposal",
    "OriginStamp",
    "ProvenanceHandle",
    "RecallBundle",
    "SituatedContextPacket",
    "SituatedOriginFrame",
    "Unavailable",
]
