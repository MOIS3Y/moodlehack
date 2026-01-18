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
from .uvicorn import UvicornServerSettings


class AppSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix=f"{paths.appname.upper()}_",
        env_nested_delimiter='__',
        toml_file=paths.settings_file,
        extra="ignore",
    )

    django: DjangoCoreSettings = Field(
        default_factory=DjangoCoreSettings
    )
    paths: AppPathSettings = Field(
        default_factory=AppPathSettings
    )
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
