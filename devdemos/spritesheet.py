import logging
import pygame

from interface import Window, Layer, Viewport, Position
from interface.renderable import Renderable
from imaging import Spritesheet
from events import Event, Orchestrator


class DemoRenderable(Renderable):
    def __init__(self, f):
        self.f = f
        self._position = Position()

        self.logger = logging.getLogger(__name__)

    @property
    def surface(self):
        return self.f

    @property
    def position(self):
        return self._position

    def handle_keypressed(self, event):
        if event[pygame.K_UP]:
            self.logger.info("KEYDOWN UP")
            self._position.shift(0, -1)
        if event[pygame.K_DOWN]:
            self.logger.info("KEYDOWN DOWN")
            self._position.shift(0, 1)
        if event[pygame.K_RIGHT]:
            self.logger.info("KEYDOWN RIGHT")
            self._position.shift(1, 0)
        if event[pygame.K_LEFT]:
            self.logger.info("KEYDOWN LEFT")
            self._position.shift(-1, 0)


def dev_spritesheet():
    logger = logging.getLogger(__name__)

    logger.info("Starting spritesheet dev demo")

    # Create our window
    window = Window("devdemo_viewport")

    viewport = Viewport()

    # window.orchestrator.subscribe(Event.KEYS_PRESSED, guy, guy.handle_keypressed)

    front_layer = Layer()
    viewport.add_layer(0, front_layer)
    window.set_viewport(viewport)

    logger.info("Loading spritesheet")
    spritesheet = Spritesheet("assets/testing/img/sheet_robot.png")
    spritesheet.slice_rows()

    # front_layer.add_renderable(guy)
    # back_layer.add_renderable(background)
    # medback_layer.add_renderable(clouds)

