"""Frozen L6 serialization fixture.

Public API is intentionally exhaustive: to_json and from_json.
"""

import json as _json
import episodic_store as _store


def to_json(result):
    if result.tag == "Success":
        obj = {
            "tag": "Success",
            "content": result.response.content,
            "source": result.response.source,
            "context": result.response.context,
            "self_position_at_encoding":
                result.response.self_position_at_encoding,
        }
    else:
        obj = {"tag": "Rejected", "reason": result.reason}
    return _json.dumps(obj, sort_keys=True).encode("utf-8")


def from_json(data):
    obj = _json.loads(data.decode("utf-8"))
    if obj["tag"] == "Success":
        response = _store._EpisodicResponse(
            content=obj["content"],
            source=obj["source"],
            context=obj["context"],
            self_position_at_encoding=obj["self_position_at_encoding"],
        )
        return _store._EpisodicResult(success=response)
    return _store._EpisodicResult(rejected_reason=obj["reason"])
