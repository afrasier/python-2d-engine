import pygame
import colorsys

import numpy as np

from imaging import KEY_HUES_LIST
from typing import List, Tuple

class PaletteColor():
    __slots__ = ['h', 's', 'v']

    def __init__(self, h: float, s: float = 1, v: float = 1):
        if h > 1:
            h = h/360.0

        self.h = h
        self.s = s
        self.v = v

    @property
    def rgb(self) -> Tuple[int, int, int]:
        '''
        Returns the RGB tuple for this color
        '''
        (r, g, b) = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        return (int(r * 255.0), int(g * 255.0), int(b * 255.0))


class Palette():
    __slots__ = ['hues', 'tolerance']

    '''
    Palette class represents a particular palette, with logic to support re-coloring sprites
    '''
    def __init__(self, hues: List[int], tolerance: int = 3):
        '''
        Specify a tolerance to give some wiggle room to the math
        '''
        self.hues: List[int] = hues
        self.tolerance: int = tolerance

    def paint_image(self, image: pygame.Surface) -> pygame.Surface:
        '''
        Paints the source image with this palette, returning a new surface
        '''
        pixel_array = self.convert_pixel_array(pygame.surfarray.array3d(image))
        surface = pygame.Surface(pixel_array.shape[:2])
        pygame.surfarray.blit_array(surface, pixel_array)

        return surface

    def convert_pixel_array(self, pixel_array: np.ndarray) -> np.ndarray:
        '''
        Converts an array of pixel RGB values based upon this palette's conversion
        '''
        shape = pixel_array.shape
        (x, y, z) = shape

        # Convert the pixel array from 3d to 2d array
        pixel_array = pixel_array.reshape(x * y, z)
        # Palette swap pixels
        pixel_array = np.apply_along_axis(self.convert_pixel, 1, pixel_array)
        # Return to 3d for painting
        pixel_array = pixel_array.reshape(x, y, z)

        # Manual loop version
        # for i in range(0, shape[0]):
        #     for j in range(0, shape[1]): 
        #         nc = self.convert_pixel(pixel_array[i, j])
        #         pixel_array[i, j] = nc

        return pixel_array

    def convert_pixel(self, color: Tuple[float, float, float]) -> Tuple[float, float, float]:
        '''
        Converts a pixel based upon HSL value
        '''
        hlv = colorsys.rgb_to_hsv(*color)
        true_hue = round(hlv[0] * 360.0)
        try:
            for i in range(0, len(KEY_HUES_LIST)):
                if i >= len(self.hues):
                    return color

                key_hue = KEY_HUES_LIST[i]

                if (key_hue - self.tolerance) <= true_hue <= (key_hue + self.tolerance):
                    new_hue = self.hues[i] - (key_hue - true_hue)
                    new_hue = min(max(0, new_hue), 360) / 360.0
                    new_color = colorsys.hsv_to_rgb(new_hue, hlv[1], hlv[2])
                    return new_color
            return color
        except IndexError: # pragma: no cover
            return color
        except ValueError: # pragma: no cover
            return color