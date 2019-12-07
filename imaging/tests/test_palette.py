import pygame
import pytest

import numpy as np

from imaging.palette import Palette, PaletteColor
from imaging import KEY_HUES_LIST


@pytest.fixture
def pixel_values():
    """
    Baseline pixel array fixture
    """
    pygame.init()

    key_hues = [240, 200, 160, 100]
    key_hues = [list(PaletteColor(kh).rgb) for kh in key_hues]

    key_hues.append([0, 0, 0])

    pixels = np.array([key_hues])

    return pixels


def test_convert_pixel_array(pixel_values: np.ndarray):
    """
    Test converting a pixel array
    """
    palette = Palette({240: 0, 200: 120, 160: 240, 100: 180}, tolerance=0)

    expected = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [0, 0, 0]]])

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, expected)


def test_convert_pixel_array_single_color(pixel_values: np.ndarray):
    """
    Test converting a pixel array with a single color
    """
    palette = Palette({240: 0}, tolerance=0)

    expected = np.array([[[255, 0, 0], pixel_values[0, 1], pixel_values[0, 2], pixel_values[0, 3], [0, 0, 0],]])

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, expected)


def test_convert_pixel_array_single_color_with_tolerances(pixel_values: np.ndarray):
    """
    Test using a palette with a single color but a tolerance; the result should map with appropriate tolerance offset
    """
    palette = Palette({240: 0}, tolerance=40)

    expected = np.array([[[255, 0, 0], [255, 0, 170], pixel_values[0, 2], pixel_values[0, 3], [0, 0, 0],]])

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, expected)


def test_convert_pixel_array_no_colors(pixel_values: np.ndarray):
    """
    Test a palette swap with no colors (identity)
    """
    palette = Palette({}, tolerance=0)

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, pixel_values)


def test_paint_image(pixel_values: np.ndarray):
    """
    Test the full image painting onto a surface
    """
    palette = Palette({240: 0, 200: 120, 160: 240, 100: 180}, tolerance=0)

    expected = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [0, 0, 0]]])

    pygame.display.set_mode((1, 1))

    surf = pygame.Surface(pixel_values.shape[:2])
    rgb_pv = Palette({}).convert_pixel_array(pixel_values)
    pygame.surfarray.blit_array(surf, rgb_pv)
    surf = palette.paint_image(surf)

    new_pixel_values = pygame.surfarray.array3d(surf)

    assert np.array_equal(new_pixel_values, expected)
