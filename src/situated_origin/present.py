"""Incremental L3-style two-lag thick-present state."""

from __future__ import annotations

from .contracts import OriginContractError, SHA256_ZERO, require_sha256


class ThickPresent:
    def __init__(self, channels: int = 8) -> None:
        if type(channels) is not int or channels < 1:
            raise OriginContractError("PRESENT_CHANNELS_INVALID")
        self.channels = channels
        self.cycle = -1
        self._current = (0.0,) * channels
        self._previous = (0.0,) * channels
        self.source_log_head = SHA256_ZERO

    def advance(self, cycle: int, features: tuple[float, ...], source_log_head: str) -> tuple[float, ...]:
        if type(cycle) is not int or cycle != self.cycle + 1:
            raise OriginContractError("PRESENT_CLOCK_MISMATCH")
        if len(features) != self.channels or any(type(value) not in (int, float) for value in features):
            raise OriginContractError("PRESENT_FEATURES_INVALID")
        require_sha256(source_log_head, "PRESENT_SOURCE_HEAD_INVALID")
        self._previous, self._current = self._current, tuple(float(value) for value in features)
        self.cycle = cycle
        self.source_log_head = source_log_head
        return self.state

    def require_source_head(self, source_log_head: str) -> None:
        if source_log_head != self.source_log_head:
            raise OriginContractError("VIEW_HEAD_STALE")

    @property
    def state(self) -> tuple[float, ...]:
        result: list[float] = []
        for current, previous in zip(self._current, self._previous):
            result.extend((current, previous))
        return tuple(result)

    @staticmethod
    def batch_reference(rows: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
        if not rows:
            return ()
        channels = len(rows[0])
        result = []
        zero = (0.0,) * channels
        for index, row in enumerate(rows):
            if len(row) != channels:
                raise OriginContractError("PRESENT_FEATURES_INVALID")
            previous = zero if index == 0 else rows[index - 1]
            state: list[float] = []
            for current, prior in zip(row, previous):
                state.extend((float(current), float(prior)))
            result.append(tuple(state))
        return tuple(result)
