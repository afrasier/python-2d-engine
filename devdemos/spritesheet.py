import logging
import pygame

import time

from interface import Window, Layer, Viewport, Position
from imaging import Spritesheet, AnimatedSprite
from events import Event, Orchestrator

from typing import List


class RenderableSwapper:
    def __init__(self, r, l, i):
        self.r = r
        self.l = l
        self.i = i

        self.l.add_renderable(self.r[self.i])

    def swap_layer(self, event):
        if event.key == pygame.K_d:
            self.l.remove_renderable(self.r[self.i])
            self.i = (self.i + 1) % len(self.r)
            self.l.add_renderable(self.r[self.i])
        if event.key == pygame.K_a:
            self.l.remove_renderable(self.r[self.i])
            self.i = (self.i - 1) % len(self.r)
            self.l.add_renderable(self.r[self.i])


class DemoRenderable(AnimatedSprite):
    def __init__(self, sprites: List[pygame.Surface], frame_data: List[int] = None):
        super().__init__(sprites, frame_data)
        self._position = Position(100, 100)

        self.logger = logging.getLogger(__name__)

    @property
    def position(self):
        return self._position

    def handle_keypressed(self, event):
        if event[pygame.K_UP]:
            self._position.shift(0, -1)
        if event[pygame.K_DOWN]:
            self._position.shift(0, 1)
        if event[pygame.K_RIGHT]:
            self._position.shift(1, 0)
        if event[pygame.K_LEFT]:
            self._position.shift(-1, 0)

    def handle_keyup(self, event):
        if event.key == pygame.K_SPACE:
            self.start_animation()
        if event.key == pygame.K_f:
            self.stop_animation()


def dev_spritesheet():
    logger = logging.getLogger(__name__)

    logger.info("Starting spritesheet dev demo")

    # Create our window
    window = Window("devdemo_viewport")

    viewport = Viewport()

    front_layer = Layer()
    viewport.add_layer(0, front_layer)
    window.set_viewport(viewport)

    logger.info("Loading spritesheet")
    sheet: List[List[pygame.Surface]] = Spritesheet.fully_slice_file(
        "assets/testing/img/sheet_robot.png", Spritesheet.BREAK_COEFFICIENT_TRANSPARENT
    )
    renderables: List[DemoRenderable] = [DemoRenderable(row, [10]) for row in sheet if len(row) != 0]
    for renderable in renderables:
        window.orchestrator.subscribe(Event.KEYS_PRESSED, renderable, renderable.handle_keypressed)
        window.orchestrator.subscribe(pygame.KEYUP, renderable, renderable.handle_keyup)

    rs = RenderableSwapper(renderables, front_layer, 0)
    window.orchestrator.subscribe(pygame.KEYUP, rs, rs.swap_layer)

    # front_layer.add_renderable(guy)
    # back_layer.add_renderable(background)
    # medback_layer.add_renderable(clouds)

