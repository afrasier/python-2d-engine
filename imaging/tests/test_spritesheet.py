import pytest
import pygame

from imaging import Spritesheet


@pytest.mark.parametrize(
    "filename,coeff,expected_shape",
    [
        ("test_sheet_pad.png", Spritesheet.BREAK_COEFFICIENT_TRANSPARENT, (2, [[(1, 1), (1, 1)], [(1, 1), (1, 1)]])),
        (
            "test_sheet_nopad.png",
            Spritesheet.BREAK_COEFFICIENT_TRANSPARENT,
            (3, [[(1, 1), (1, 1), (1, 1)], [(1, 1), (1, 1), (1, 1)], [(1, 1), (1, 1), (1, 1)]]),
        ),
        (
            "test_sheet_black_nopad.png",
            Spritesheet.BREAK_COEFFICIENT_SOLID,
            (3, [[(5, 5), (7, 5), (6, 5)], [(5, 5), (7, 5), (6, 5)], [(5, 8), (7, 8), (6, 8)]]),
        ),
        (
            "test_sheet_black_pad.png",
            Spritesheet.BREAK_COEFFICIENT_SOLID,
            (3, [[(4, 4), (7, 4), (5, 4)], [(4, 5), (7, 5), (5, 5)], [(4, 7), (7, 7), (5, 7)]]),
        ),
    ],
)
def test_slicing(filename, coeff, expected_shape):
    sliced = Spritesheet.fully_slice_file(f"assets/testing/img/{filename}", coeff)
    assert len(sliced) == expected_shape[0]
    for i in range(0, len(sliced)):
        for j in range(0, len(sliced[i])):
            s = (sliced[i][j].get_width(), sliced[i][j].get_height())
            assert s == expected_shape[1][i][j]
