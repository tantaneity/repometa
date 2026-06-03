from __future__ import annotations

import httpx

from .constants import (
    GITHUB_ACCEPT_HEADER,
    GITHUB_API_BASE_URL,
    GITHUB_API_VERSION,
    GITHUB_API_VERSION_HEADER,
    HTTP_TIMEOUT_SECONDS,
    REPO_PATH_TEMPLATE,
    TOPICS_BODY_KEY,
    TOPICS_PATH_TEMPLATE,
)
from .errors import GitHubApiError
from .models import RepoRef


def create_http_client(token: str) -> httpx.Client:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": GITHUB_ACCEPT_HEADER,
        GITHUB_API_VERSION_HEADER: GITHUB_API_VERSION,
    }
    return httpx.Client(
        base_url=GITHUB_API_BASE_URL,
        headers=headers,
        timeout=HTTP_TIMEOUT_SECONDS,
    )


class GitHubClient:
    def __init__(self, http_client: httpx.Client) -> None:
        self._http = http_client

    def set_topics(self, repo: RepoRef, topics: list[str]) -> list[str]:
        path = TOPICS_PATH_TEMPLATE.format(owner=repo.owner, name=repo.name)
        response = self._http.put(path, json={TOPICS_BODY_KEY: topics})
        self._raise_for_status(response)
        payload = response.json()
        return payload.get(TOPICS_BODY_KEY, [])

    def update_repo(self, repo: RepoRef, fields: dict[str, str]) -> None:
        if not fields:
            return
        path = REPO_PATH_TEMPLATE.format(owner=repo.owner, name=repo.name)
        response = self._http.patch(path, json=fields)
        self._raise_for_status(response)

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.is_success:
            return
        raise GitHubApiError(response.status_code, _extract_detail(response))


def _extract_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text.strip() or response.reason_phrase
    if isinstance(payload, dict):
        message = payload.get("message")
        if isinstance(message, str):
            return message
    return response.reason_phrase
