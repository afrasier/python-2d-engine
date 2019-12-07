import logging
import pygame
import sys

from settings.config import APP_DATA
from interface import Viewport
from events import Event, Orchestrator
from threading import Thread


class Window:
    def __init__(self, title: str, width: int = 1000, height: int = 1000):
        """
        Initializes a window
        """
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing pygame mixer")
        pygame.mixer.pre_init(44100, -16, 2, 3072)
        pygame.mixer.init()

        self.logger.debug("Initializing pygame")
        pygame.init()

        self.viewport: Viewport = None

        # Create screen
        self.logger.debug(f"Creating screen with dimensions: {width} x {height}")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.orchestrator: Orchestrator = Orchestrator.get_instance()
        self.render_clock: pygame.time.Clock = pygame.time.Clock()
        self.logic_clock: pygame.time.Clock = pygame.time.Clock()

        self.exit_signal = False

        self.render_thread: Thread = Thread(target=self.run_rendering, name="WindowRenderingThread", args=())
        self.logic_thread: Thread = Thread(target=self.run_logic, name="WindowLogicThread", args=())

        self.render_thread.start()
        self.logic_thread.start()

    def close(self) -> None:
        self.logger.info("Gracefully shutting down...")

        self.render_thread.join()
        self.logic_thread.join()
        sys.exit(0)

    def set_viewport(self, viewport: Viewport) -> None:
        """
        Sets the viewport
        """
        self.viewport = viewport

    def run_rendering(self) -> None:
        """
        Runs the window, rendering to screen
        """
        while not self.exit_signal:
            # Blank out the screen
            self.screen.fill(0)

            # Render everything our viewport has
            if self.viewport:
                self.viewport.blit(self.screen)

            pygame.display.flip()
            self.render_clock.tick(APP_DATA.get("clocks", {}).get("rendering", 60))  # Max out at 60 FPS

    def run_logic(self) -> None:
        """
        Runs and handles logic updates
        """
        while not self.exit_signal:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_signal = True

                # Broadcast the pygame event via the orchestrator
                self.orchestrator.emit(event.type, event)

            # Broadcast all currently held down keys
            self.orchestrator.emit(Event.KEYS_PRESSED, pygame.key.get_pressed())
            self.logic_clock.tick(APP_DATA.get("clocks", {}).get("logic", 100))
