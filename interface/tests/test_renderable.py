import pytest
import pygame

from interface.renderable import Renderable
from interface import Anchor, Position


class DemoRenderable(Renderable):
    def __init__(self, f, a):
        self.f = f
        self._position = Position()
        self._anchor = a

    @property
    def surface(self):
        return self.f

    @property
    def position(self):
        return self._position

    @property
    def anchor(self):
        return self._anchor


@pytest.mark.parametrize(
    "anchor,expected_renderable_location",
    [
        (Anchor.TOP_LEFT, (0, 0)),
        (Anchor.TOP_CENTER, (-5, 0)),
        (Anchor.TOP_RIGHT, (-10, 0)),
        (Anchor.CENTER_LEFT, (0, -5)),
        (Anchor.CENTER, (-5, -5)),
        (Anchor.CENTER_RIGHT, (-10, -5)),
        (Anchor.BOTTOM_LEFT, (0, -10)),
        (Anchor.BOTTOM_CENTER, (-5, -10)),
        (Anchor.BOTTOM_RIGHT, (-10, -10)),
    ],
)
def test_anchored_positions(anchor, expected_renderable_location):
    dr = DemoRenderable(pygame.surface.Surface((10, 10)), anchor)
    ap = dr.anchored_position
    assert ap.x == expected_renderable_location[0]
    assert ap.y == expected_renderable_location[1]


@pytest.mark.parametrize(
    "anchor,test_click_position,expected",
    [
        (Anchor.TOP_LEFT, (5, 5), True),
        (Anchor.TOP_LEFT, (11, 5), False),
        (Anchor.TOP_LEFT, (-1, 5), False),
        (Anchor.TOP_LEFT, (5, 11), False),
        (Anchor.TOP_LEFT, (5, -1), False),
        (Anchor.TOP_LEFT, (10, 10), True),
        (Anchor.BOTTOM_RIGHT, (-5, -5), True),
        (Anchor.BOTTOM_RIGHT, (-11, -5), False),
        (Anchor.BOTTOM_RIGHT, (1, -5), False),
        (Anchor.BOTTOM_RIGHT, (-5, -11), False),
        (Anchor.BOTTOM_RIGHT, (-5, 1), False),
        (Anchor.BOTTOM_RIGHT, (-10, -10), True),
    ],
)
def test_position_intersects(anchor, test_click_position, expected):
    dr = DemoRenderable(pygame.surface.Surface((10, 10)), anchor)
    assert dr.position_intersects(Position(*test_click_position)) == expected
