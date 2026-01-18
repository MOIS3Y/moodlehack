"""File system paths management for app"""

from .paths import AppPaths

paths = AppPaths(ensure_exists=True)

__all__ = ['paths', 'AppPaths']
