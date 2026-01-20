import asyncio
import ssl
from configparser import RawConfigParser
from os import PathLike
from typing import IO, Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn.config import (
    LOGGING_CONFIG,
    SSL_PROTOCOL_VERSION,
    HTTPProtocolType,
    InterfaceType,
    LifespanType,
    LoopFactoryType,
    WSProtocolType,
)


# [uvicorn.logging]
class UvicornLoggingSettings(BaseSettings):
    """Logging configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    log_config: dict[str, Any] | str | RawConfigParser | IO[Any] | None = (
        Field(default=LOGGING_CONFIG)
    )
    log_level: str | int | None = Field(default=None)
    access_log: bool = Field(default=True)
    use_colors: bool | None = Field(default=None)


# [uvicorn.ssl]
class UvicornSslSettings(BaseSettings):
    """SSL configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    ssl_keyfile: str | PathLike[str] | None = Field(default=None)
    ssl_certfile: str | PathLike[str] | None = Field(default=None)
    ssl_keyfile_password: str | None = Field(default=None)
    ssl_version: int = Field(default=SSL_PROTOCOL_VERSION)
    ssl_cert_reqs: int = Field(default=ssl.CERT_NONE)
    ssl_ca_certs: str | None = Field(default=None)
    ssl_ciphers: str = Field(default="TLSv1")



# [uvicorn.server.protocol]
class UvicornProtocolSettings(BaseSettings):
    """Protocol configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    # HTTP protocol
    http: type[asyncio.Protocol] | HTTPProtocolType = Field(default="auto")
    h11_max_incomplete_event_size: int | None = Field(default=None)

    # WebSocket protocol
    ws: type[asyncio.Protocol] | WSProtocolType = Field(default="auto")
    ws_max_size: int = Field(default=16777216)
    ws_max_queue: int = Field(default=32)
    ws_ping_interval: float | None = Field(default=20.0)
    ws_ping_timeout: float | None = Field(default=20.0)
    ws_per_message_deflate: bool = Field(default=True)

    lifespan: LifespanType = Field(default="auto")


# [uvicorn.server.performance]
class UvicornPerformanceSettings(BaseSettings):
    """Performance configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    workers: int | None = Field(default=None)
    limit_concurrency: int | None = Field(default=None)
    limit_max_requests: int | None = Field(default=None)
    backlog: int = Field(default=2048)
    timeout_keep_alive: int = Field(default=5)
    timeout_graceful_shutdown: int | None = Field(default=None)


# [uvicorn.server.advanced]
class UvicornAdvancedSettings(BaseSettings):
    """Advanced configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    # Server interface
    interface: InterfaceType = Field(default="auto")
    loop: LoopFactoryType = Field(default="auto")
    uds: str | None = Field(default=None)  # UNIX domain socket path
    fd: int | None = Field(default=None)

    # Development settings
    reload: bool = Field(default=False)
    reload_dirs: list[str] | str | None = Field(default=None)
    reload_delay: float = Field(default=0.25)
    reload_includes: list[str] | str | None = Field(default=None)
    reload_excludes: list[str] | str | None = Field(default=None)
    app_dir: str | None = Field(default=None)  # Look for APP in this directory

    # Headers and security
    proxy_headers: bool = Field(default=True)
    server_header: bool = Field(default=True)
    date_header: bool = Field(default=True)
    forwarded_allow_ips: list[str] | str | None = Field(default=None)
    root_path: str = Field(default="")

    # Additional
    headers: list[tuple[str, str]] | None = Field(default=None)
    factory: bool = Field(default=False)
    env_file: str | PathLike[str] | None = Field(default=None)


# [uvicorn.server]
class UvicornServerSettings(BaseSettings):
    """Server configuration for Uvicorn"""
    model_config = SettingsConfigDict(extra='ignore')

    # Basic server settings
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    # Sub-configurations
    logging: UvicornLoggingSettings = Field(
        default_factory=UvicornLoggingSettings
    )
    ssl: UvicornSslSettings = Field(
        default_factory=UvicornSslSettings
    )
    protocol: UvicornProtocolSettings = Field(
        default_factory=UvicornProtocolSettings
    )
    performance: UvicornPerformanceSettings = Field(
        default_factory=UvicornPerformanceSettings
    )
    advanced: UvicornAdvancedSettings = Field(
        default_factory=UvicornAdvancedSettings
    )

    @property
    def as_dict(self) -> dict:
        """Convert to dictionary for uvicorn.run()"""
        config_data = {}

        # Extract basic settings from main class
        config_data['host'] = self.host
        config_data['port'] = self.port

        # Extract settings from subclasses
        config_data.update(self.logging.model_dump(exclude_none=True))
        config_data.update(self.ssl.model_dump(exclude_none=True))
        config_data.update(self.protocol.model_dump(exclude_none=True))
        config_data.update(self.performance.model_dump(exclude_none=True))
        config_data.update(self.advanced.model_dump(exclude_none=True))

        return config_data
