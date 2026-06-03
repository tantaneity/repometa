from pathlib import Path


class RepometaError(Exception):
    pass


class RepoReferenceError(RepometaError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid repository reference: '{value}'. Expected 'owner/name'.")


class TokenNotFoundError(RepometaError):
    def __init__(self) -> None:
        super().__init__(
            "GitHub token not found. Set GITHUB_TOKEN or sign in via 'git credential'."
        )


class TopicValidationError(RepometaError):
    pass


class PresetNotFoundError(RepometaError):
    def __init__(self, name: str, available: list[str]) -> None:
        known = ", ".join(available) or "none"
        super().__init__(f"Preset '{name}' not found. Available: {known}.")


class PresetConfigError(RepometaError):
    def __init__(self, path: Path, reason: str) -> None:
        super().__init__(f"Invalid presets config at {path}: {reason}")


class GitHubApiError(RepometaError):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(f"GitHub API error {status_code}: {detail}")
        self.status_code = status_code
