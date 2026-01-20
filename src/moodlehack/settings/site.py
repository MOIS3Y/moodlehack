from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings

from moodlehack.fs import paths


class SiteSettings(BaseSettings):
    """
    Application branding and site-wide metadata.
    Mapped to [site] section in TOML.
    """

    # Branding
    label: str = Field(default=paths.appname)
    tagline: str = Field(default="Knowledge Base")

    # Metadata automatically synced from paths/init
    app_name: str = Field(default=paths.appname)
    version: str = Field(default=paths.version)

    @property
    def as_dict(self) -> dict[str, Any]:
        """
        Return site settings as a dictionary
        for Django settings consistency.
        """
        return {k.upper(): v for k, v in self.model_dump().items()}
