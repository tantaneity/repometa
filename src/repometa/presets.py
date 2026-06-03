from __future__ import annotations

import tomllib
from pathlib import Path

from .constants import DEFAULT_PRESETS, PRESETS_TABLE_KEY
from .errors import PresetConfigError, PresetNotFoundError


class PresetStore:
    def __init__(self, presets: dict[str, list[str]]) -> None:
        self._presets = presets

    @classmethod
    def load(cls, user_presets_path: Path) -> PresetStore:
        merged = {name: list(topics) for name, topics in DEFAULT_PRESETS.items()}
        merged.update(cls._read_user_presets(user_presets_path))
        return cls(merged)

    def get(self, name: str) -> list[str]:
        if name not in self._presets:
            raise PresetNotFoundError(name, sorted(self._presets))
        return list(self._presets[name])

    def all(self) -> dict[str, list[str]]:
        return {name: list(topics) for name, topics in sorted(self._presets.items())}

    @staticmethod
    def _read_user_presets(path: Path) -> dict[str, list[str]]:
        if not path.exists():
            return {}
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as error:
            raise PresetConfigError(path, str(error)) from error
        section = data.get(PRESETS_TABLE_KEY, {})
        if not isinstance(section, dict):
            raise PresetConfigError(path, f"'{PRESETS_TABLE_KEY}' must be a table.")
        result: dict[str, list[str]] = {}
        for name, topics in section.items():
            if not isinstance(topics, list) or not all(isinstance(item, str) for item in topics):
                raise PresetConfigError(path, f"Preset '{name}' must be a list of strings.")
            result[name] = topics
        return result
