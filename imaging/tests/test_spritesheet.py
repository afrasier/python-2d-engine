import pytest
import pygame

from imaging import Spritesheet


@pytest.mark.parametrize(
    "filename,coeff,expected_shape",
    [
        ("test_sheet_pad.png", Spritesheet.BREAK_COEFFICIENT_TRANSPARENT, (2, [2, 2])),
        ("test_sheet_nopad.png", Spritesheet.BREAK_COEFFICIENT_TRANSPARENT, (3, [3, 3, 3])),
        ("test_sheet_black_nopad.png", Spritesheet.BREAK_COEFFICIENT_SOLID, (3, [3, 3, 3])),
        ("test_sheet_black_pad.png", Spritesheet.BREAK_COEFFICIENT_SOLID, (3, [3, 3, 3])),
    ],
)
def test_slicing(filename, coeff, expected_shape):
    sliced = Spritesheet.fully_slice_file(f"assets/testing/img/{filename}", coeff)
    assert len(sliced) == expected_shape[0]
    assert [len(row) for row in sliced] == expected_shape[1]
