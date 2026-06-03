from repometa.models import RepoRef
from repometa.presets import PresetStore
from repometa.service import ApplyRequest, ApplyService


class FakeWriter:
    def __init__(self) -> None:
        self.topics: list[str] = []
        self.fields: dict[str, str] = {}
        self.set_topics_calls = 0

    def set_topics(self, repo: RepoRef, topics: list[str]) -> list[str]:
        self.set_topics_calls += 1
        self.topics = topics
        return topics

    def update_repo(self, repo: RepoRef, fields: dict[str, str]) -> None:
        self.fields = fields


def _service(writer: FakeWriter) -> ApplyService:
    store = PresetStore({"fastapi": ["fastapi", "python"]})
    return ApplyService(writer, store)


def should_merge_preset_with_extra_topics_deduped():
    writer = FakeWriter()
    request = ApplyRequest(
        repo=RepoRef("owner", "name"),
        preset="fastapi",
        extra_topics=["python", "redis"],
        description=None,
        homepage=None,
    )

    result = _service(writer).apply(request)

    assert result.applied_topics == ["fastapi", "python", "redis"]
    assert writer.topics == ["fastapi", "python", "redis"]


def should_not_touch_topics_when_none_provided():
    writer = FakeWriter()
    request = ApplyRequest(
        repo=RepoRef("owner", "name"),
        preset=None,
        extra_topics=[],
        description="hello",
        homepage=None,
    )

    result = _service(writer).apply(request)

    assert writer.set_topics_calls == 0
    assert result.updated_fields == ["description"]
    assert writer.fields == {"description": "hello"}
