from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import CONFIG_DIR, ENV_FILE_NAME, PRESETS_FILENAME


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    github_token: str | None = None

    @property
    def presets_path(self) -> Path:
        return CONFIG_DIR / PRESETS_FILENAME
