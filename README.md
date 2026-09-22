# MoodleHack

MoodleHack is a self-hosted repository for Moodle test answers, featuring a
fast search interface and a REST API for data exchange.

It is designed to be a lightweight, standalone application that can be
deployed with minimal configuration.

## Features

-   Fast, full-text search for questions and answers.
-   REST API with OpenAPI schema documentation.
-   Answers organized by category, year, and month.
-   Status tracking for answers (e.g., Actual, Outdated, Draft).
-   Designed to run as an embedded service without an external web server
    like Nginx or Caddy.

## Installation

The recommended and simplest way to run MoodleHack is by using Docker.

### Docker Compose

For a declarative setup, you can use `docker-compose`. Create a
`docker-compose.yml` file with the following content:

```yaml
services:
  moodlehack:
    image: mois3y/moodlehack:0.2.1rc3
    container_name: moodlehack
    restart: unless-stopped
    ports:
      - "8000:8000"
    # To use environment variables from a file, uncomment the next line.
    # See examples/example.env for a template.
    # env_file:
    #   - ./.env
    volumes:
      - moodlehack_data:/app/data
      # Optional: Mount a local settings file.
      # - ./settings.toml:/app/config/moodlehack/settings.toml
    environment:
      - MOODLEHACK_DJANGO__SECRET_KEY=a-very-secret-key-that-you-must-change
      - MOODLEHACK_DJANGO__TIME_ZONE=UTC
      # - MOODLEHACK_SITE__NAME="My Custom Name"

volumes:
  moodlehack_data: {}
```

Save the file and run `docker-compose up -d`. This will use a named Docker
volume (`moodlehack_data`) to persist data.

## First-Time Setup

After starting the container for the first time, you need to create a
superuser to access the admin interface.

Run the following command:

```shell
docker exec -it moodlehack moodlehack createsuperuser
```

You will be prompted to enter a username, email, and password for the new
superuser account.

## Configuration

The application can be configured using environment variables or a
`settings.toml` file.

### Configuration Examples

The `examples/` directory in this project's repository contains template
files that you can use as a starting point:
-   `settings.toml`: An example of a TOML configuration file.
-   `example.env`: An example of a file for environment variables, which
    can be used with `docker-compose`'s `env_file` directive.

### Environment Variables

All settings can be controlled via environment variables. The variables must
be prefixed with `MOODLEHACK_`. Use a double underscore `__` to separate
nested keys.

**Example:**
```shell
export MOODLEHACK_SITE__NAME="My Answers"
export MOODLEHACK_DJANGO__TIME_ZONE="Europe/Moscow"
```

### Settings File

Alternatively, you can provide a `settings.toml` file. When using Docker,
you can mount it into the container. The application expects the file at
`/app/config/moodlehack/settings.toml`.

**Example `settings.toml`:**
```toml
[site]
name = "My Answers"
label = "Moodle Answers"

[django]
time_zone = "Europe/Moscow"
secret_key = "a-very-secret-key-that-you-must-change"
```

## Uvicorn configuration

Uvicorn options are read from a flat `[uvicorn]` section:

```toml
[uvicorn]
host = "0.0.0.0"
port = 8000
workers = 2
access_log = false
```

Environment variables override file values, for example
`MOODLEHACK_UVICORN__WORKERS=4` or
`MOODLEHACK_UVICORN__ACCESS_LOG=false`. Use JSON for lists in environment
variables, such as `MOODLEHACK_UVICORN__RELOAD_DIRS='["src"]'`.

Accepted options, types and defaults come from the installed Uvicorn
version. Only explicitly configured values are passed to the server.
The application controls `app`; it cannot be overridden. Unknown options
are rejected. Command-line `--host` and `--port` override configuration.

When upgrading, move keys from the old `[uvicorn.logging]`,
`[uvicorn.ssl]`, `[uvicorn.protocol]`, `[uvicorn.performance]` and
`[uvicorn.advanced]` tables into `[uvicorn]`. Remove the corresponding
group segment from environment variable names, for example
`MOODLEHACK_UVICORN__LOGGING__ACCESS_LOG` becomes
`MOODLEHACK_UVICORN__ACCESS_LOG`. Old grouped options are rejected.

Run the Uvicorn configuration tests with:

```shell
uv run moodlehack test moodlehack.settings
```

## Development and dependency updates

Python 3.12 or newer is required. The Nix development shell uses Python 3.14
and provides uv and gettext:

```shell
nix develop
uv sync --locked
```

After upgrading from the old Nix shell, re-enter the shell to clear its
Python package paths.

Update the minimum dependency versions in `pyproject.toml`, then run:

```shell
uv lock --upgrade
nix flake update
uv lock --check
uv build
nix flake check
nix build .#moodlehack
nix build .#dockerImage
```

Commit both lockfiles. Nix uses uv2nix to build the application's runtime
dependencies from `uv.lock`; build tools and Nix inputs are pinned through
`flake.lock`. Nix builds include compiled translation catalogs.
All Nix configuration is in `flake.nix`. Use `nix build` and `nix develop`.
Docker image builds require Linux.
Nix outputs support x86_64 Linux, aarch64 Linux and Apple Silicon macOS;
the updated nixos-unstable input no longer supports Intel macOS.

## Project Status

This is an unstable release but is functional. A stable release will be
available after further testing and real-world validation.
