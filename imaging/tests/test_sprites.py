import pygame
import time

from imaging import Sprite, AnimatedSprite
from interface import Anchor


class SimpleSprite(Sprite):
    @property
    def position(self):
        return None


class SimpleAnimatedSprite(AnimatedSprite):
    @property
    def position(self):
        return None


def test_sprite():
    sprite = SimpleSprite(pygame.surface.Surface((10, 10)))
    assert sprite.surface.get_width() == 10
    assert sprite.surface.get_height() == 10
    assert sprite.anchor == Anchor.TOP_LEFT


def test_animated_sprite_default_framedata():
    frames = [pygame.surface.Surface((1, 1)), pygame.surface.Surface((2, 2))]
    sprite = SimpleAnimatedSprite(frames)

    assert sprite.frame_data == [10]


def test_animated_sprite():
    frames = [pygame.surface.Surface((1, 1)), pygame.surface.Surface((2, 2))]
    sprite = SimpleAnimatedSprite(frames, [1])

    assert sprite.surface.get_width() == 1
    assert sprite.current_frame == 0

    sprite.start_animation()
    time.sleep(0.1)

    assert sprite.surface.get_width() == 2
    assert sprite.current_frame == 1

    time.sleep(1)
    sprite.stop_animation()

    assert sprite.surface.get_width() == 1
    assert sprite.current_frame == 0
