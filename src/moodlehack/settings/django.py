from pathlib import Path
from typing import Any, Literal

from django.utils.translation import gettext_lazy as _
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from moodlehack.fs import paths


# [django.cache]
class DjangoCacheSettings(BaseSettings):
    """
    Cache configuration settings for Django.
    Supports LocMem (default), File-based (XDG), and Dummy backends.
    """
    backend: str = Field(default="locmem")
    location: str = Field(default="django_cache")

    @field_validator('backend', mode='before')
    @classmethod
    def normalize_backend(cls, v: str) -> str:
        """Map short names to full Django cache backend paths."""
        backend_aliases = {
            "locmem": "django.core.cache.backends.locmem.LocMemCache",
            "file": "django.core.cache.backends.filebased.FileBasedCache",
            "dummy": "django.core.cache.backends.dummy.DummyCache",
        }
        return backend_aliases.get(v.lower(), v)

    @property
    def as_dict(self) -> dict[str, Any]:
        """Convert to Django CACHES format using AppPaths for file storage."""
        backend_path = self.normalize_backend(self.backend)
        final_location = self.location

        if "FileBasedCache" in backend_path:
            cache_path = paths.cache_dir / self.location
            paths.ensure_exists(cache_path, mode=0o700)
            final_location = str(cache_path)

        return {
            "default": {
                "BACKEND": backend_path,
                "LOCATION": final_location,
            }
        }

# [django.database]
class DjangoDatabaseSettings(BaseSettings):
    """Database configuration settings for Django"""
    engine: str = Field(default="sqlite3")
    name: str | Path = Field(default="db.sqlite3")
    user: str | None = Field(default=None)
    password: str | None = Field(default=None)
    host: str | None = Field(default=None)
    port: int | None = Field(default=None)
    options: dict[str, Any] | None = Field(default_factory=dict)

    @field_validator('engine', mode='before')
    @classmethod
    def normalize_engine(cls, v: str) -> str:
        """Normalize database engine names to full Django backend paths"""
        engine_aliases = {
            'postgresql': 'django.db.backends.postgresql',
            'postgres': 'django.db.backends.postgresql',
            'sqlite3': 'django.db.backends.sqlite3',
            'sqlite': 'django.db.backends.sqlite3',
            'mysql': 'django.db.backends.mysql',
            'oracle': 'django.db.backends.oracle',
        }
        return engine_aliases.get(v, v)

    @field_validator('name', mode='before')
    @classmethod
    def validate_name_based_on_engine(cls, v: str | Path, info):
        """
        Auto-convert database name to Path for SQLite,
        keep string for other databases
        """
        engine = info.data.get('engine', '')
        if (
            'sqlite3' in engine
            and isinstance(v, str)
            and not v.startswith((':', 'file:'))
        ):
            database_dir = paths.data_dir / "db"
            return paths.ensure_exists(database_dir, mode=0o700) / v
        return v

    @property
    def as_dict(self) -> dict[str, Any]:
        """Convert to Django DATABASES format dictionary"""
        config: dict[str, Any] = {
            'ENGINE': self.engine,
            'NAME': str(self.name),
        }

        if self.options:
            config['OPTIONS'] = self.options

        if 'sqlite3' not in self.engine:
            if self.user:
                config['USER'] = self.user
            if self.password:
                config['PASSWORD'] = self.password
            if self.host:
                config['HOST'] = self.host
            if self.port:
                config['PORT'] = self.port

        return {'default': config}


# [django.data]
class DjangoDataFilesSettings(BaseSettings):
    """Settings for Django data file uploads and forms"""
    data_upload_max_number_fields: int = Field(default=10_000)

    @property
    def default_auto_field(self) -> str:
        "Default primary key field type for models."
        return "django.db.models.BigAutoField"


# [django.email]
class DjangoEmailSettings(BaseSettings):
    """Email configuration settings for Django"""
    backend: str = Field(default="console")
    host: str = Field(default="localhost")
    port: int = Field(default=25)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    use_tls: bool = Field(default=False)
    use_ssl: bool = Field(default=False)
    ssl_keyfile: str | None = Field(default=None)
    ssl_certfile: str | None = Field(default=None)
    from_email: str | None = Field(default=None)
    timeout: int | None = Field(default=None)

    @field_validator('backend', mode='before')
    @classmethod
    def normalize_backend(cls, v: str) -> str:
        """Normalize email backend names to full Django backend paths"""
        backend_aliases = {
            "console": "django.core.mail.backends.console.EmailBackend",
            "smtp": "django.core.mail.backends.smtp.EmailBackend",
            "file": "django.core.mail.backends.filebased.EmailBackend",
            "memory": "django.core.mail.backends.locmem.EmailBackend",
            "dummy": "django.core.mail.backends.dummy.EmailBackend",
        }
        return backend_aliases.get(v, v)


# [django.i18n]
class DjangoI18nSettings(BaseSettings):
    """
    Internationalization and localization settings for Django.
    Allows user to choose between supported languages.
    """
    language_code: Literal["ru", "en"] = Field(
        default="ru",
        description="Default language code for the application"
    )
    time_zone: str = Field(
        default="UTC",
        description="Time zone for the application"
    )

    @property
    def use_tz(self) -> bool:
        """Enable timezone support"""
        return True

    @property
    def use_i18n(self) -> bool:
        """Enable internationalization"""
        return True

    @property
    def languages(self) -> list[tuple[str, str]]:
        """
        Supported language localizations.
        Used by Django for translation discovery.
        """
        return [
            ("en", str(_("English"))),
            ("ru", str(_("Russian")))
        ]

    @property
    def locale_paths(self) -> list[Path]:
        "A list of directories where Django looks for translation files"
        return [
            paths.base_dir / "locale"
        ]

# [django.media]
class DjangoMediaSettings(BaseSettings):
    """Media files configuration for Django"""
    root: Path = Field(default_factory=lambda: paths.data_dir / "media")
    url: str = Field(default="/media/")

    @field_validator("root", mode="after")
    @classmethod
    def ensure_media_dir(cls, v: Path) -> Path:
        """Ensure media directory exists with proper permissions"""
        return paths.ensure_exists(v, mode=0o755)


# [django.static]
class DjangoStaticSettings(BaseSettings):
    """Static files configuration for Django"""
    root: Path = Field(default_factory=lambda: paths.data_dir / "static")
    url: str = Field(default="/static/")

    @field_validator("root", mode="after")
    @classmethod
    def ensure_static_dir(cls, v: Path) -> Path:
        """Ensure static directory exists with proper permissions"""
        return paths.ensure_exists(v, mode=0o755)

    @property
    def staticfiles_finders(self) -> list[str]:
        """Static files finders configuration"""
        return [
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ]

    @property
    def staticfiles_dirs(self) -> list[Path]:
        """Additional directories for static files collection"""
        return []


# [django.crispy]
class DjangoCrispySettings(BaseSettings):
    """Crispy forms configuration."""
    @property
    def template_pack(self) -> str:
        return "bootstrap5"

    @property
    def allowed_template_packs(self) -> str:
        return "bootstrap5"


# [django.rest_framework]
class DjangoRestFrameworkSettings(BaseSettings):
    """
    DRF configuration settings.
    Renderers are determined by the 'browsable' flag.
    """
    browsable: bool = Field(default=False)

    @property
    def as_dict(self) -> dict:
        # Base renderers/parsers for JSON API
        renderers = ["rest_framework.renderers.JSONRenderer"]
        parsers = ["rest_framework.parsers.JSONParser"]

        if self.browsable:
            gui = "rest_framework.renderers.BrowsableAPIRenderer"
            renderers.append(gui)
            parsers.append(gui)

        return {
            "DEFAULT_RENDERER_CLASSES": renderers,
            "DEFAULT_PARSER_CLASSES": parsers,
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework.authentication.SessionAuthentication",
                "rest_framework.authentication.BasicAuthentication",
            ],
            "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
            "DEFAULT_FILTER_BACKENDS": [
                "django_filters.rest_framework.DjangoFilterBackend"
            ],
        }

# [django.spectacular]
class DjangoSpectacularSettings(BaseSettings):
    """DRF Spectacular (OpenAPI) internal configuration"""
    @property
    def as_dict(self) -> dict:
        return {
            "TITLE": "AKVOLABEAN",  # TODO: make it editable
            "DESCRIPTION": "Internal API for moodle answering service",
            "VERSION": "0.2.0",  # TODO: make it depends of __version__
            "SERVE_INCLUDE_SCHEMA": True,
            "SERVE_PUBLIC": False,
            "SWAGGER_UI_SETTINGS": {"filter": True},
        }


# [django]
class DjangoCoreSettings(BaseSettings):
    """Core Django application settings"""

    allowed_hosts: list[str] = Field(
        default_factory=lambda: [
            "localhost",
            "127.0.0.1"
        ]
    )
    csrf_trusted_origins: list[str] = Field(
        default_factory=lambda: []
    )
    internal_ips: list[str] = Field(
        default_factory=lambda: [
            "127.0.0.1",
        ]
    )

    debug: bool = Field(default=False)
    secret_key: str = Field(default="j9QGbvM9Z4otb47-change-me")

    cache: DjangoCacheSettings = Field(
        default_factory=DjangoCacheSettings
    )
    data: DjangoDataFilesSettings = Field(
        default_factory=DjangoDataFilesSettings
    )
    database: DjangoDatabaseSettings = Field(
        default_factory=DjangoDatabaseSettings
    )
    email: DjangoEmailSettings = Field(
        default_factory=DjangoEmailSettings
    )
    i18n: DjangoI18nSettings = Field(
        default_factory=DjangoI18nSettings
    )
    media: DjangoMediaSettings = Field(
        default_factory=DjangoMediaSettings
    )
    static: DjangoStaticSettings = Field(
        default_factory=DjangoStaticSettings
    )
    crispy: DjangoCrispySettings = Field(
        default_factory=DjangoCrispySettings
    )
    rest_framework: DjangoRestFrameworkSettings = Field(
        default_factory=DjangoRestFrameworkSettings
    )
    spectacular: DjangoSpectacularSettings = Field(
        default_factory=DjangoSpectacularSettings
    )

    @property
    def auth_password_validators(self) -> list[dict]:
        """Password validation configuration"""
        lib_path = "django.contrib.auth.password_validation"
        validators = [
            {
                "NAME": f"{lib_path}.UserAttributeSimilarityValidator",
            },
            {
                "NAME": f"{lib_path}.MinimumLengthValidator",
            },
            {
                "NAME": f"{lib_path}.CommonPasswordValidator",
            },
            {
                "NAME": f"{lib_path}.NumericPasswordValidator",
            },
        ]
        return validators

    @property
    def installed_apps(self) -> list[str]:
        """List of installed Django applications"""
        return [
            # local:
            "moodlehack.accounts",
            "moodlehack.answers",
            "moodlehack.serve",
            # django:
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            # extra:
            "rest_framework",
            "rest_framework.authtoken",
            "drf_spectacular",
            "django_filters",
            "crispy_forms",
            "crispy_bootstrap5",
        ]

    @property
    def middleware(self) -> list[str]:
        """Middleware configuration for Django"""
        return [
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]

    @property
    def templates(self) -> list[dict[str, Any]]:
        """Template configuration for Django"""
        return [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    paths.base_dir / "templates",
                ],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ]

    @property
    def root_urlconf(self) -> str:
        """Root URL configuration module"""
        return "moodlehack.core.urls"

    @property
    def storages(self) -> dict[str, dict]:
        """Storage backend configuration"""
        files_storage_lib: str = "django.core.files.storage"
        staticfiles_storage_lib: str = "django.contrib.staticfiles.storage"
        return {
            "default": {
                "BACKEND": f"{files_storage_lib}.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": f"{staticfiles_storage_lib}.StaticFilesStorage",
            },
        }
