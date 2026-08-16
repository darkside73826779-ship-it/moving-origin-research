"""Frozen L6 episodic-store fixture.

Public API is intentionally exhaustive: query_episodic and
query_episodic_batch. All other names are private.
"""

_FIXTURE = {}


class _EpisodicResponse:
    def __init__(self, content, source, context, self_position_at_encoding):
        self.content = content
        self.source = source
        self.context = context
        self.self_position_at_encoding = self_position_at_encoding


class _EpisodicResult:
    def __init__(self, success=None, rejected_reason=None):
        if success is not None:
            self.tag = "Success"
            self.response = success
            self.reason = None
        else:
            self.tag = "Rejected"
            self.response = None
            self.reason = rejected_reason


def _install_fixture(mapping):
    _FIXTURE.clear()
    _FIXTURE.update(mapping)


def _clear_fixture():
    _FIXTURE.clear()


def query_episodic(query):
    if query is None:
        return _EpisodicResult(rejected_reason="registry_unavailable")
    if query == "":
        return _EpisodicResult(rejected_reason="not_found")
    content = _FIXTURE.get(
        query, {"query": query, "data": "fixture_content"})
    response = _EpisodicResponse(
        content=content,
        source="append",
        context={
            "chain_position": 0,
            "prev_hash": "0" * 64,
            "self_hash": "1" * 64,
        },
        self_position_at_encoding={"cycle": 0, "landmark_relative": {}},
    )
    return _EpisodicResult(success=response)


def query_episodic_batch(queries):
    return [query_episodic(query) for query in queries]
