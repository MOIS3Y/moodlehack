from typing import Any

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from moodlehack.fs import paths

from .django import DjangoCoreSettings
from .paths import AppPathSettings
from .site import SiteSettings
from .uvicorn import UvicornServerSettings


class AppSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix=f"{paths.appname.upper()}_",
        env_nested_delimiter='__',
        toml_file=paths.settings_file,
        extra="ignore",
    )

    django: DjangoCoreSettings = Field(default_factory=DjangoCoreSettings)
    paths: AppPathSettings = Field(default_factory=AppPathSettings)
    site: SiteSettings = Field(default_factory=SiteSettings)
    uvicorn: UvicornServerSettings = Field(
        default_factory=UvicornServerSettings
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        toml_settings = TomlConfigSettingsSource(settings_cls)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            toml_settings,
            file_secret_settings,
        )

    def model_post_init(self, __context: Any) -> None:
        """
        Override configuration after loading from all sources.

        This method is used to synchronize dependent settings, calculate
        dynamic defaults, and ensure consistency across different
        configuration sections.
        """
        # Sync Spectacular API title with Site label if not explicitly set
        if self.django.spectacular.title is None:
            self.django.spectacular.title = self.site.label

        # Automatically enable Browsable API in DEBUG mode
        # only if the user hasn't explicitly set 'browsable'
        if self.django.rest_framework.browsable is None:
            self.django.rest_framework.browsable = self.django.debug
