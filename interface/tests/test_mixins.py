import pygame
import pytest

from datetime import datetime

from imaging import Sprite
from interface import Position
from interface.mixins import ClickAwareMixin, HoverAwareMixin


@pytest.fixture
def mixin_sprite():
    class SimpleSprite(Sprite, ClickAwareMixin, HoverAwareMixin):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.click_count = 0

        def _ClickAwareMixin__handle_click(self, event):
            self.click_count = self.click_count + 1

        @property
        def position(self):
            return Position()

    return SimpleSprite(pygame.surface.Surface((10, 10)))


@pytest.mark.parametrize(
    "click_pos,is_clicked", [((5, 5), True), ((10, 10), True), ((-5, -5), False), ((-10, -10), False)],
)
def test_click(mixin_sprite, click_pos, is_clicked):
    e = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=click_pos)

    if mixin_sprite.clickable:
        assert is_clicked == mixin_sprite.handle_click(e)


@pytest.mark.freeze_time
@pytest.mark.parametrize(
    "move_pos,is_hovered", [((5, 5), True), ((10, 10), True), ((-5, -5), False), ((-10, -10), False)],
)
def test_hover(mixin_sprite, freezer, move_pos, is_hovered):
    e = pygame.event.Event(pygame.MOUSEMOTION, pos=move_pos)

    if mixin_sprite.hoverable:
        assert mixin_sprite.time_hovered == None
        freezer.move_to("2019-01-01 12:00:00")
        assert mixin_sprite.handle_mousemove(e) == is_hovered
        assert mixin_sprite.is_hovered == is_hovered

        if is_hovered:
            freezer.move_to("2019-01-01 12:00:10")
            assert (datetime.now() - mixin_sprite.time_hovered).seconds == 10

