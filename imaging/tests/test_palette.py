import pygame
import pytest

import numpy as np

from imaging.palette import Palette, PaletteColor
from imaging import KEY_HUES_LIST


@pytest.fixture
def pixel_values():
    pygame.init()

    key_hues = [240, 200, 160, 100]
    key_hues = [list(PaletteColor(kh).rgb) for kh in key_hues]

    key_hues.append([0, 0, 0])

    pixels = np.array([key_hues])

    return pixels


def test_convert_pixel_array(pixel_values: np.ndarray):
    palette = Palette({240: 0, 200: 120, 160: 240, 100: 180}, tolerance=0)

    expected = np.array(
        [[[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [0, 0, 0]]]
    )

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, expected)


def test_convert_pixel_array_single_color(pixel_values: np.ndarray):
    palette = Palette({0: 0}, tolerance=0)

    expected = np.array(
        [
            [
                [255, 0, 0],
                pixel_values[0, 1],
                pixel_values[0, 2],
                pixel_values[0, 3],
                [0, 0, 0],
            ]
        ]
    )

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, expected)


def test_convert_pixel_array_no_colors(pixel_values: np.ndarray):
    palette = Palette({}, tolerance=0)

    new_pixel_values = palette.convert_pixel_array(pixel_values)

    assert np.array_equal(new_pixel_values, pixel_values)


def test_paint_image(pixel_values: np.ndarray):
    palette = Palette({240: 0, 200: 120, 160: 240, 100: 180}, tolerance=0)

    expected = np.array(
        [[[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [0, 0, 0]]]
    )

    surf = pygame.Surface(pixel_values.shape[:2])
    rgb_pv = Palette([]).convert_pixel_array(pixel_values)
    pygame.surfarray.blit_array(surf, rgb_pv)
    surf = palette.paint_image(surf)

    new_pixel_values = pygame.surfarray.array3d(surf)

    assert np.array_equal(new_pixel_values, expected)
