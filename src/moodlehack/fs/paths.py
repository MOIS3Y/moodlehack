import os
import sys
from functools import cached_property
from pathlib import Path

from platformdirs import PlatformDirs


class AppPaths:
    """
    Simple adapter for PlatformDirs with privilege-aware paths.
    Provides system/user paths with optional automatic directory creation.
    Automatically detects app name from project directory.
    """

    def __init__(self, appname: str = None, ensure_exists: bool = False):
        """
        Initialize AppPaths.

        Args:
            appname: Name of the application/package.
                If None, automatically detected from project directory name.
            ensure_exists: If True, PlatformDirs will create basic directories
        """
        self._ensure_exists = ensure_exists

        if appname is None:
            self.appname = self._detect_appname()
        else:
            self.appname = appname

        self._dirs = PlatformDirs(
            appname=self.appname,
            ensure_exists=ensure_exists,
            roaming=False,
            multipath=True,
        )

    def _detect_appname(self) -> str:
        """
        Detect app name from project directory.

        Returns:
            Name of the application (top level package name)
            (directory name containing manage.py and __init__.py)
        """
        base_dir = self.base_dir
        if base_dir == Path(__file__).parent:
            return Path.cwd().name
        return base_dir.name

    @cached_property
    def is_root(self) -> bool:
        """Check if running as root (cached)."""
        return os.getuid() == 0

    @cached_property
    def base_dir(self) -> Path:
        """
        Project root directory - where manage.py and __init__.py are together.
        """
        current = Path(__file__).parent

        for parent in [current] + list(current.parents):
            manage_py = parent / "manage.py"
            init_py = parent / "__init__.py"

            if manage_py.exists() and init_py.exists():
                return parent

        for parent in [current] + list(current.parents):
            if (parent / "manage.py").exists():
                return parent

        return current

    def _path(self, name: str, root_fallback: str = None) -> Path:
        """
        Universal method for getting paths with privilege awareness.
        """
        if self.is_root:
            if hasattr(self._dirs, f"site_{name}_path"):
                path = getattr(self._dirs, f"site_{name}_path")()
            elif root_fallback:
                path_str = root_fallback.format(package=self.appname)
                path = Path(path_str)
            else:
                path = getattr(self._dirs, f"user_{name}_path")
        else:
            path = getattr(self._dirs, f"user_{name}_path")

        return path

    def ensure_exists(self, path: Path, mode: int = 0o755) -> Path:
        """
        Ensure directory exists with specified permissions.
        Skipped during management commands that don't require
        filesystem side effects.
        """

        # Commands that should not trigger directory creation
        skip_commands = {
            "makemessages",
            "compilemessages",
        }

        if any(cmd in sys.argv for cmd in skip_commands):
            return path

        try:
            path.mkdir(parents=True, exist_ok=True)
            if path.exists():
                path.chmod(mode)
        except (PermissionError, OSError) as e:
            error_msg = (
                f"Failed to create directory {path}: {e}\n"
                f"Make sure you have proper permissions or run with "
                f"appropriate user."
            )
            raise type(e)(error_msg) from e

        return path

    @cached_property
    def settings_file(self) -> Path:
        """Path to settings.toml configuration file."""
        env_var = f"{self.appname.upper()}_SETTINGS_FILE"
        if env_file := os.getenv(env_var):
            return Path(env_file)
        return self.config_dir / "settings.toml"

    @cached_property
    def config_dir(self) -> Path:
        """Directory for configuration files."""
        return self._path("config")

    @cached_property
    def data_dir(self) -> Path:
        """Directory for application data."""
        return self._path("data")

    @cached_property
    def cache_dir(self) -> Path:
        """Directory for cache."""
        return self._path("cache")

    @cached_property
    def state_dir(self) -> Path:
        """Directory for state data."""
        return self._path("state", root_fallback="{package}")

    @cached_property
    def log_dir(self) -> Path:
        """Directory for logs."""
        return self._path("log", root_fallback="/var/log/{package}")

    @property
    def as_dict(self) -> dict[str, Path]:
        """
        Get all paths as dictionary.
        """
        return {
            "base_dir": self.base_dir,
            "config_dir": self.config_dir,
            "settings_file": self.settings_file,
            "data_dir": self.data_dir,
            "cache_dir": self.cache_dir,
            "state_dir": self.state_dir,
            "log_dir": self.log_dir,
        }

    def __repr__(self) -> str:
        return f"AppPaths(appname='{self.appname}', is_root={self.is_root})"
