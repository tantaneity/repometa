# repometa

One command to stamp a GitHub repo with topics, a description and a homepage. No more clicking topics in one by one, no more gluing a giant `gh repo edit --add-topic ... --add-topic ...` by hand. Presets cover the stacks you reach for every week.

```
repometa apply --repo tantaneity/repometa --preset fastapi
repometa apply --repo owner/name --topics python,docker --desc "tiny cli"
repometa preset list
```

## Why

I spin up a repo roughly once a week and my hands keep doing the same dance: same topic set per stack, same description shape, sometimes a homepage link. So this just does it in one shot, and the topics stay in sync across similar projects.

## Install

`uv` pulls straight from the repo into an isolated tool venv and drops the command on your PATH:

```
uv tool install git+https://github.com/tantaneity/repometa
```

A push to the repo is the "release". Nothing to build, no token to juggle.

## Auth

The CLI needs a GitHub token with `repo` scope (a fine-grained token with Administration write works too). It looks in two places, in order:

1. `GITHUB_TOKEN`, from the environment or a local `.env`
2. `git credential fill` for `github.com`, if you are already signed in to git

So if git already knows your GitHub login, you usually need to set nothing. Otherwise drop a token in `.env` (see `.env.example`) or export it.

`gh` is never required, which matters on Windows where it may not sit on PATH.

## Usage

`apply` is the workhorse:

```
--repo      -r   Target as owner/name (required)
--preset    -p   Named topic set to apply
--topics    -t   Extra topics, comma-separated
--desc      -d   Repository description
--homepage       Homepage URL
```

Preset and extra topics merge, then dedupe:

```
repometa apply -r owner/name -p fastapi -t auth,redis
```

That sends `fastapi, python, sqlalchemy, alembic, docker, async, auth, redis`. Topics get lowercased and validated before anything hits the API (GitHub only allows lowercase letters, digits and hyphens, up to 50 chars, up to 20 per repo). Leave out `--preset` and `--topics` and existing topics stay untouched, only the metadata you pass gets written.

## Presets

Built in:

- `fastapi` → fastapi, python, sqlalchemy, alembic, docker, async
- `nestjs` → nestjs, typescript, nodejs, postgresql, docker
- `unity` → unity, csharp, gamedev
- `react` → react, typescript, frontend, vite

List everything (built-ins plus yours):

```
repometa preset list
```

### Your own presets

Drop a `presets.toml` at `~/.config/repometa/presets.toml`. Same name as a built-in overrides it.

```toml
[presets]
go = ["go", "golang", "backend"]
django = ["django", "python", "postgresql", "celery"]
```

## How it talks to GitHub

Topics ride their own endpoint, `PUT /repos/{owner}/{repo}/topics`. Description and homepage go through `PATCH /repos/{owner}/{repo}`. They are separate calls because topics never travel through the PATCH body.

## Develop

```
uv sync
uv run pytest
```

## Publish to PyPI (optional)

Tag a version and an Action publishes it through Trusted Publishing (OIDC, no long-lived token):

```
git tag v0.1.0
git push --tags
```

Set up the pending publisher on PyPI first and add a `pypi` environment in the repo settings. The workflow lives in `.github/workflows/publish.yml`.
