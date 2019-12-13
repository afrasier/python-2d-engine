import pygame

from interface.renderable import Renderable
from interface import Anchor
from threading import Thread

from typing import List


class Sprite(Renderable):
    """
    Sprite represents a sprite
    """

    def __init__(self, image: pygame.Surface, anchor: Anchor = Anchor.TOP_LEFT):
        """
        Creates an animated sprite

        :param image: An image for this sprite
        :param anchor: The anchor position for this sprite image
        """
        self._surface = image
        self._anchor = anchor

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @property
    def anchor(self) -> Anchor:
        return self._anchor


class AnimatedSprite(Renderable):
    """
    AnimatedSprite supports animated sprites
    """

    def __init__(self, sprites: List[pygame.Surface], frame_data: List[int] = None):
        """
        Creates an animated sprite

        :param sprites: A list of sprites representing each frame of animation
        :param frame_data: A list of integers representing the speed of each frame
        """
        if frame_data is None:
            frame_data = [10]

        self.current_frame = 0
        self.sprites = sprites
        self.frame_count = len(sprites)
        self.frame_data = frame_data

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.animating: bool = False
        self.animation_thread: Thread = None

    @property
    def surface(self) -> pygame.Surface:
        """
        Returns the current frame
        """
        return self.sprites[self.current_frame]

    def start_animation(self) -> None:
        """
        Starts the animation
        """
        if not self.animating:
            self.animating = True
            self.animation_thread = Thread(target=self.__run_animation, name=f"AnimatedSprite_{__name__}", args=())
            self.animation_thread.start()

    def stop_animation(self) -> None:
        """
        Stops the animation
        """
        self.animating = False
        self.animation_thread = None

    def __run_animation(self) -> None:
        """
        Thread which runs the animation
        """
        while self.animating:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.clock.tick(self.frame_data[self.current_frame % len(self.frame_data)])  # Wait for our framedata spec

