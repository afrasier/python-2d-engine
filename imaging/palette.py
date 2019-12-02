import pygame
import colorsys

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
        Paints the source image with this palette, provided image must comply to source hues
        '''
        pixel_array = pygame.surfarray.array3d(image)
        shape = pixel_array.shape

        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                nc = self.convert_pixel(pixel_array[i, j])
                pixel_array[i, j] = nc
        
        surface = pygame.Surface((shape[0], shape[1]))
        pygame.surfarray.blit_array(surface, pixel_array)
        return surface

    def convert_pixel(self, color: Tuple[float, float, float]) -> Tuple[float, float, float]:
        '''
        Converts a pixel based upon HSL value
        '''
        hlv = colorsys.rgb_to_hsv(*color)
        true_hue = int(hlv[0] * 360)
        try:
            for i in range(0, len(KEY_HUES_LIST)):
                if i >= len(self.hues):
                    return color

                key_hue = KEY_HUES_LIST[i]

                if (key_hue - self.tolerance) <= true_hue <= (key_hue + self.tolerance):
                    new_hue = self.hues[i] - (key_hue - true_hue)
                    new_hue = min(max(0, new_hue), 360) / 360.0
                    return colorsys.hsv_to_rgb(new_hue, hlv[1], hlv[2])
            return color
        except IndexError:
            print(true_hue)
            return color
        except ValueError:
            print(true_hue)
            return color