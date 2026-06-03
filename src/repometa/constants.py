from pathlib import Path

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"
GITHUB_ACCEPT_HEADER = "application/vnd.github+json"
GITHUB_API_VERSION_HEADER = "X-GitHub-Api-Version"
HTTP_TIMEOUT_SECONDS = 15.0

TOPICS_PATH_TEMPLATE = "/repos/{owner}/{name}/topics"
REPO_PATH_TEMPLATE = "/repos/{owner}/{name}"
TOPICS_BODY_KEY = "names"
DESCRIPTION_FIELD = "description"
HOMEPAGE_FIELD = "homepage"

MAX_TOPICS_PER_REPO = 20
MAX_TOPIC_LENGTH = 50
TOPIC_PATTERN = r"^[a-z0-9][a-z0-9-]*$"

REPO_REF_SEPARATOR = "/"
TOPICS_INPUT_SEPARATOR = ","

ENV_TOKEN_NAME = "GITHUB_TOKEN"
ENV_FILE_NAME = ".env"

GIT_CREDENTIAL_PROTOCOL = "https"
GIT_CREDENTIAL_HOST = "github.com"
GIT_CREDENTIAL_PASSWORD_PREFIX = "password="

CONFIG_DIR = Path.home() / ".config" / "repometa"
PRESETS_FILENAME = "presets.toml"
PRESETS_TABLE_KEY = "presets"

EXIT_FAILURE = 1

DEFAULT_PRESETS: dict[str, list[str]] = {
    "fastapi": ["fastapi", "python", "sqlalchemy", "alembic", "docker", "async"],
    "nestjs": ["nestjs", "typescript", "nodejs", "postgresql", "docker"],
    "unity": ["unity", "csharp", "gamedev"],
    "react": ["react", "typescript", "frontend", "vite"],
}
