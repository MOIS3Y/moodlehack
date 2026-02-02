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
    image: mois3y/moodlehack:0.2.1rc2
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

## Project Status

This is an unstable release but is functional. A stable release will be
available after further testing and real-world validation.