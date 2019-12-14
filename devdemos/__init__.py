"""
Dev package contains demo functions
"""

from devdemos.palette import dev_palette
from devdemos.viewport import dev_viewport
from devdemos.spritesheet import dev_spritesheet
from devdemos.buttons import dev_button

from typing import Callable, Dict

DEV_DEMOS: Dict[str, Callable] = {
    "palette": dev_palette,
    "viewport": dev_viewport,
    "spritesheet": dev_spritesheet,
    "button": dev_button,
}
