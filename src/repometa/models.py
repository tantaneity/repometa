from __future__ import annotations

from dataclasses import dataclass

from .constants import REPO_REF_SEPARATOR
from .errors import RepoReferenceError


@dataclass(frozen=True)
class RepoRef:
    owner: str
    name: str

    @classmethod
    def parse(cls, value: str) -> RepoRef:
        parts = value.split(REPO_REF_SEPARATOR)
        if len(parts) != 2 or not all(part.strip() for part in parts):
            raise RepoReferenceError(value)
        owner, name = parts
        return cls(owner=owner.strip(), name=name.strip())

    def __str__(self) -> str:
        return f"{self.owner}{REPO_REF_SEPARATOR}{self.name}"
