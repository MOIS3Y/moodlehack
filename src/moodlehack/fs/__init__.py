"""File system paths management for app"""

from moodlehack import __version__

from .paths import AppPaths

paths = AppPaths(version=__version__)

__all__ = ['paths', 'AppPaths']
