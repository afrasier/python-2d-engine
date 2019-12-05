import pygame
import colorsys

import numpy as np

from typing import List, Tuple, Dict


class PaletteColor:
    __slots__ = ["h", "s", "v"]

    def __init__(self, h: float, s: float = 1, v: float = 1):
        if h > 1:
            h = h / 360.0

        self.h = h
        self.s = s
        self.v = v

    @property
    def rgb(self) -> Tuple[int, int, int]:
        """
        Returns the RGB tuple for this color
        """
        (r, g, b) = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        return (round(r * 255.0), round(g * 255.0), round(b * 255.0))


class Palette:
    __slots__ = ["hues", "tolerance"]

    """
    Palette class represents a particular palette, with logic to support re-coloring sprites
    """

    def __init__(self, hues: Dict[int, int], tolerance: int = 3):
        """
        Specify a tolerance to give some wiggle room to the math
        """
        self.hues: Dict[int, int] = hues
        self.tolerance: int = tolerance

        # Expand our dict to include tolerances
        if tolerance > 0:
            base_hues = list(self.hues.keys())
            for hue in base_hues:
                for tolerated_hue in range((hue - tolerance), (hue + tolerance + 1)):
                    target_hue = self.hues.get(hue) - (hue - tolerated_hue)
                    self.hues[tolerated_hue % 360] = target_hue % 360

    def paint_image(self, image: pygame.Surface) -> pygame.Surface:
        """
        Paints the source image with this palette, returning a new surface
        """
        # Store the image's alpha
        alphas = pygame.surfarray.array_alpha(image)
        # Convert image to pixel array and swap colors
        pixel_array = self.convert_pixel_array(pygame.surfarray.array3d(image))
        # Remap pixel array to surface and add alpha channel
        surface = pygame.Surface.convert_alpha(pygame.surfarray.make_surface(pixel_array))
        # Copy original alpha to new surface's alpha
        surface_alpha_reference = pygame.surfarray.pixels_alpha(surface)
        np.copyto(surface_alpha_reference, alphas)
        del surface_alpha_reference  # Unlock the surface by removing the reference to alphas
        del alphas
        return surface

    def convert_pixel_array(self, pixel_array: np.ndarray) -> np.ndarray:
        """
        Converts an array of pixel RGB values based upon this palette's conversion
        """
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
        """
        Converts a pixel based upon HSL value
        """
        (h, l, v) = colorsys.rgb_to_hsv(*color)
        true_hue = round(h * 360.0)
        (r, g, b) = colorsys.hsv_to_rgb(self.hues.get(true_hue, true_hue) / 360.0, l, v)
        return (round(r), round(g), round(b))

