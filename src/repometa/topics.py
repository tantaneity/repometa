from __future__ import annotations

import re
from collections.abc import Iterable

from .constants import MAX_TOPIC_LENGTH, MAX_TOPICS_PER_REPO, TOPIC_PATTERN
from .errors import TopicValidationError

_TOPIC_REGEX = re.compile(TOPIC_PATTERN)


def normalize_topics(raw_topics: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for raw in raw_topics:
        topic = raw.strip().lower()
        if not topic:
            continue
        _validate_topic(topic)
        if topic not in normalized:
            normalized.append(topic)
    if len(normalized) > MAX_TOPICS_PER_REPO:
        raise TopicValidationError(
            f"Too many topics: {len(normalized)} (max {MAX_TOPICS_PER_REPO})."
        )
    return normalized


def _validate_topic(topic: str) -> None:
    if len(topic) > MAX_TOPIC_LENGTH:
        raise TopicValidationError(
            f"Topic '{topic}' exceeds {MAX_TOPIC_LENGTH} characters."
        )
    if not _TOPIC_REGEX.match(topic):
        raise TopicValidationError(
            f"Topic '{topic}' is invalid: use lowercase letters, digits and hyphens, "
            "starting with a letter or digit."
        )
