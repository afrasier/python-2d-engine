from typing import List
from imaging.palette import Palette

from enum import Enum

class KEY_HUES(Enum):
    '''
    Key hues represent the hue value that imaging logic uses to process images
    '''
    PRIMARY = 240
    SECONDARY = 200
    TERTIARY = 160
    QUATERNARY = 100

KEY_HUES_LIST: List[int] = [v.value for v in KEY_HUES]