from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .constants import DESCRIPTION_FIELD, HOMEPAGE_FIELD
from .models import RepoRef
from .presets import PresetStore
from .topics import normalize_topics


class RepoMetadataWriter(Protocol):
    def set_topics(self, repo: RepoRef, topics: list[str]) -> list[str]: ...

    def update_repo(self, repo: RepoRef, fields: dict[str, str]) -> None: ...


@dataclass(frozen=True)
class ApplyRequest:
    repo: RepoRef
    preset: str | None
    extra_topics: list[str]
    description: str | None
    homepage: str | None


@dataclass(frozen=True)
class ApplyResult:
    applied_topics: list[str]
    updated_fields: list[str]


class ApplyService:
    def __init__(self, writer: RepoMetadataWriter, preset_store: PresetStore) -> None:
        self._writer = writer
        self._presets = preset_store

    def apply(self, request: ApplyRequest) -> ApplyResult:
        topics = self._collect_topics(request)
        applied = self._writer.set_topics(request.repo, topics) if topics else []
        fields = self._collect_fields(request)
        self._writer.update_repo(request.repo, fields)
        return ApplyResult(applied_topics=applied, updated_fields=sorted(fields))

    def _collect_topics(self, request: ApplyRequest) -> list[str]:
        raw: list[str] = []
        if request.preset:
            raw.extend(self._presets.get(request.preset))
        raw.extend(request.extra_topics)
        return normalize_topics(raw)

    @staticmethod
    def _collect_fields(request: ApplyRequest) -> dict[str, str]:
        fields: dict[str, str] = {}
        if request.description is not None:
            fields[DESCRIPTION_FIELD] = request.description
        if request.homepage is not None:
            fields[HOMEPAGE_FIELD] = request.homepage
        return fields
