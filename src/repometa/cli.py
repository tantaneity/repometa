from __future__ import annotations

import typer

from .auth import TokenResolver
from .config import Settings
from .constants import EXIT_FAILURE, TOPICS_INPUT_SEPARATOR
from .errors import RepometaError
from .github import GitHubClient, create_http_client
from .models import RepoRef
from .presets import PresetStore
from .service import ApplyRequest, ApplyResult, ApplyService

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Set GitHub repository topics, description and homepage in one command.",
)
preset_app = typer.Typer(no_args_is_help=True, help="Inspect stack presets.")
app.add_typer(preset_app, name="preset")


@app.command()
def apply(
    repo: str = typer.Option(..., "--repo", "-r", help="Repository as owner/name."),
    preset: str | None = typer.Option(None, "--preset", "-p", help="Preset name to apply."),
    topics: str | None = typer.Option(
        None, "--topics", "-t", help="Extra topics, comma-separated."
    ),
    desc: str | None = typer.Option(None, "--desc", "-d", help="Repository description."),
    homepage: str | None = typer.Option(None, "--homepage", help="Homepage URL."),
) -> None:
    try:
        settings = Settings()
        token = TokenResolver(settings.github_token).resolve()
        store = PresetStore.load(settings.presets_path)
        with create_http_client(token) as http_client:
            service = ApplyService(GitHubClient(http_client), store)
            result = service.apply(
                ApplyRequest(
                    repo=RepoRef.parse(repo),
                    preset=preset,
                    extra_topics=_parse_topics(topics),
                    description=desc,
                    homepage=homepage,
                )
            )
    except RepometaError as error:
        _fail(error)
    _print_result(repo, result)


@preset_app.command("list")
def preset_list() -> None:
    try:
        store = PresetStore.load(Settings().presets_path)
    except RepometaError as error:
        _fail(error)
    for name, topics in store.all().items():
        typer.echo(f"{name}: {', '.join(topics)}")


def _parse_topics(value: str | None) -> list[str]:
    if not value:
        return []
    return [item for item in value.split(TOPICS_INPUT_SEPARATOR) if item.strip()]


def _print_result(repo: str, result: ApplyResult) -> None:
    if result.applied_topics:
        typer.secho(
            f"Topics on {repo}: {', '.join(result.applied_topics)}",
            fg=typer.colors.GREEN,
        )
    if result.updated_fields:
        typer.secho(
            f"Updated {repo}: {', '.join(result.updated_fields)}",
            fg=typer.colors.GREEN,
        )
    if not result.applied_topics and not result.updated_fields:
        typer.secho("Nothing to apply.", fg=typer.colors.YELLOW)


def _fail(error: RepometaError) -> None:
    typer.secho(str(error), fg=typer.colors.RED, err=True)
    raise typer.Exit(code=EXIT_FAILURE) from error
