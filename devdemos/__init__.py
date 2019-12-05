"""
Dev package contains demo functions
"""

from devdemos.palette import dev_palette

from typing import Callable, Dict

DEV_DEMOS: Dict[str, Callable] = {"palette": dev_palette}
