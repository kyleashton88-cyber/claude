"""Script and transcript linter. It never records a legal sign-off."""

from .lint import lint_path

__all__ = ["lint_path"]
