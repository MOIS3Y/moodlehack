from pathlib import Path

from pydantic_settings import BaseSettings

from moodlehack.fs import paths


class AppPathSettings(BaseSettings):
    """
    Adapter for AppPaths to be used within Pydantic settings.
    Exposes system-detected paths as configuration constants.
    """

    @property
    def as_dict(self) -> dict[str, Path]:
        """Return all detected paths as a dictionary with uppercase keys."""
        return {key.upper(): val for key, val in paths.as_dict.items()}
