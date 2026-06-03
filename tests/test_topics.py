import pytest

from repometa.errors import TopicValidationError
from repometa.topics import normalize_topics


def should_lowercase_and_dedupe_when_topics_repeat():
    assert normalize_topics(["Python", "python", " DOCKER "]) == ["python", "docker"]


def should_drop_empty_entries_when_present():
    assert normalize_topics(["", "  ", "python"]) == ["python"]


def should_raise_when_topic_has_invalid_characters():
    with pytest.raises(TopicValidationError):
        normalize_topics(["py thon"])


def should_raise_when_topic_starts_with_hyphen():
    with pytest.raises(TopicValidationError):
        normalize_topics(["-python"])


def should_raise_when_too_many_topics():
    with pytest.raises(TopicValidationError):
        normalize_topics([f"topic-{index}" for index in range(21)])
