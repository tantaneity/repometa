from __future__ import annotations

import subprocess

from .constants import (
    GIT_CREDENTIAL_HOST,
    GIT_CREDENTIAL_PASSWORD_PREFIX,
    GIT_CREDENTIAL_PROTOCOL,
)
from .errors import TokenNotFoundError


class TokenResolver:
    def __init__(self, env_token: str | None) -> None:
        self._env_token = env_token

    def resolve(self) -> str:
        if self._env_token:
            return self._env_token
        credential_token = self._read_from_git_credential()
        if credential_token:
            return credential_token
        raise TokenNotFoundError()

    @staticmethod
    def _read_from_git_credential() -> str | None:
        request = (
            f"protocol={GIT_CREDENTIAL_PROTOCOL}\n"
            f"host={GIT_CREDENTIAL_HOST}\n"
            "\n"
        )
        try:
            result = subprocess.run(
                ["git", "credential", "fill"],
                input=request,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return None
        if result.returncode != 0:
            return None
        for line in result.stdout.splitlines():
            if line.startswith(GIT_CREDENTIAL_PASSWORD_PREFIX):
                return line[len(GIT_CREDENTIAL_PASSWORD_PREFIX):].strip()
        return None
