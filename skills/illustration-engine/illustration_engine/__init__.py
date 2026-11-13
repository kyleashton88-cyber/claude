"""In-house illustration engine.

Draw educational diagrams as SVG and PNG. This package does not call an
image API and does not write course stills.
"""

from .parser import parse
from .render import render_prompt, render_spec
from .spec import TYPES, Spec
from .theme import set_default

__all__ = ["TYPES", "Spec", "parse", "render_prompt", "render_spec", "set_default"]
