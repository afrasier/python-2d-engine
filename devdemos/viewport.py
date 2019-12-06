import logging
import pygame

from interface import Window, Layer, Viewport, Position
from interface.renderable import Renderable
from events import Event, Orchestrator


class DemoRenderable(Renderable):
    def __init__(self, f):
        self.f = pygame.image.load(f)
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


class DemoViewportMover:
    def __init__(self, vp):
        self.vp = vp
        self.logger = logging.getLogger(__name__)

    def handle_keypressed(self, event):
        if event[pygame.K_w]:
            self.logger.info("KEYDOWN W")
            self.vp.position.shift(0, -1)
        if event[pygame.K_s]:
            self.logger.info("KEYDOWN S")
            self.vp.position.shift(0, 1)
        if event[pygame.K_a]:
            self.logger.info("KEYDOWN A")
            self.vp.position.shift(-1, 0)
        if event[pygame.K_d]:
            self.logger.info("KEYDOWN D")
            self.vp.position.shift(1, 0)


def dev_viewport():
    logger = logging.getLogger(__name__)

    logger.info("Starting viewport demo; use WASD to shift viewport")

    # Create our window
    window = Window("devdemo_viewport")

    viewport = Viewport()
    dvpm = DemoViewportMover(viewport)

    guy = DemoRenderable("assets/testing/img/guy.png")
    guy.position.shift(50, 50)
    background = DemoRenderable("assets/testing/img/background.png")
    clouds = DemoRenderable("assets/testing/img/clouds_mid.png")

    window.orchestrator.subscribe(Event.KEYS_PRESSED, dvpm, dvpm.handle_keypressed)
    window.orchestrator.subscribe(Event.KEYS_PRESSED, guy, guy.handle_keypressed)

    front_layer = Layer()
    medback_layer = Layer(motion_scale=(1.5, 1))
    back_layer = Layer(motion_scale=(0.25, 1))

    viewport.add_layer(0, front_layer)
    viewport.add_layer(10, medback_layer)
    viewport.add_layer(20, back_layer)

    window.set_viewport(viewport)

    front_layer.add_renderable(guy)
    back_layer.add_renderable(background)
    medback_layer.add_renderable(clouds)
