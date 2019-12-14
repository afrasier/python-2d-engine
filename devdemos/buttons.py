import logging
import pygame

from imaging import Spritesheet
from interface import Window, Layer, Viewport, Position
from interface.renderable import Renderable
from interface.mixins import ClickAwareMixin, HoverAwareMixin
from events import Event, Orchestrator, ChronoOrchestrator


class StatefulButton(Renderable, ClickAwareMixin, HoverAwareMixin):
    def __init__(self, f):
        self.button_states = f
        self.button_state = 0
        self._position = Position(50, 50)

        self.logger = logging.getLogger(__name__)

    def set_button_state(self, state):
        self.button_state = state

    def _handle_click(self, event):
        self.logger.info(f"You clicked on me with event:\n\t{event}")
        co: ChronoOrchestrator = ChronoOrchestrator.get_instance()
        co.add_trigger(self.set_button_state, cb_args=(self.button_state,), seconds=5)
        self.button_state = 2

    def _handle_hover(self, event, is_hovered):
        if is_hovered:
            self.button_state = 1
        else:
            self.button_state = 0

    @property
    def surface(self):
        return self.button_states[self.button_state]

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


def dev_button():
    logger = logging.getLogger(__name__)

    logger.info("Starting button demo")

    # Create our window
    window = Window("devdemo_button")

    viewport = Viewport()

    buttons = Spritesheet.fully_slice_file(
        "assets/testing/img/button_spritesheet.png", break_coefficient=Spritesheet.BREAK_COEFFICIENT_TRANSPARENT
    )

    button = StatefulButton(buttons[0])

    window.orchestrator.subscribe(Event.KEYS_PRESSED, button, button.handle_keypressed)
    window.orchestrator.subscribe(pygame.MOUSEBUTTONUP, viewport, viewport.mouse_event_dispersal)
    window.orchestrator.subscribe(pygame.MOUSEMOTION, viewport, viewport.mouse_event_dispersal)

    front_layer = Layer()

    viewport.add_layer(0, front_layer)

    window.set_viewport(viewport)

    front_layer.add_renderable(button)

    viewport.active = True
