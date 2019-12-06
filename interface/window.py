import pygame

from interface import Viewport
from events import Event, Orchestrator
from threading import Thread


class Window:
    def __init__(self, title: str):
        """
        Initializes a window
        """
        # Init pygame
        pygame.mixer.pre_init(44100, -16, 2, 3072)
        pygame.mixer.init()
        pygame.init()

        self.viewport: Viewport = None

        # Create screen
        self.screen: pygame.Surface = pygame.display.set_mode((0, 0))
        pygame.display.set_caption(title)

        self.orchestrator: Orchestrator = Orchestrator.get_instance()

        self.run_thread = Thread(target=self.run, name="WindowThread", args=())

        self.run_thread.start()

    def run(self) -> None:
        """
        Runs the window, rendering to screen
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    # Broadcast the pygame event via the orchestrator
                    self.orchestrator.emit(event.type, event)

            # Render everything our viewport has
            if self.viewport:
                self.viewport.blit(self.screen)

            pygame.display.flip()
            pygame.time.Clock.tick(60)  # Max out at 60 FPS

