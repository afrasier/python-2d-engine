import pygame

from enum import IntEnum
from interface import Renderable, Position

from typing import Dict


class Layer:
    """
    Layer represents an individual layer of renderables
    """

    def __init__(self, motion_scale: float = 1):
        # Scales the motion of the camera (useful for parallax or static items (scale = 0))
        self.motion_scale: float = motion_scale
        # Dictionary of renderables organized by id (dictionaries maintain their order in Python 3.6)
        self.renderables: Dict[int, Renderable] = {}

    def add_renderable(self, renderable: Renderable) -> None:
        """
        Adds a renderable to this layer
        """
        renderable_id = id(renderable)
        self.renderables[renderable_id] = renderable

    def remove_renderable(self, renderable: Renderable) -> None:
        """
        Removes a renderable from this layer
        """
        renderable_id = id(renderable)
        if renderable_id in self.renderables:
            del self.renderables[renderable_id]

    def blit(self, viewport_position: Position, surface: pygame.Surface) -> None:
        """
        Renders this layer's renderables onto the given surface
        """
        for renderable in self.renderables.values():
            rendering_position = (
                renderable.position.x - viewport_position.x,
                renderable.position.y - viewport_position.y,
            )

            # Since this rendering position would mark the top left of the renderable, we can do a quick
            # check to see if the rendering position > surface width/height
            if rendering_position[0] > surface.get_width() or rendering_position[1] > surface.get_height():
                continue

            surface.blit(renderable.surface, rendering_position)


class Viewport:
    """
    viewport.py

    Represents a viewport; all items wishing to be rendered should be registered with this class

    Items are rendered based upon their layer, in the order they were added to that layer
    """

    def __init__(self):
        self.position: Position = Position()

    def blit(self, surface: pygame.Surface) -> None:
        """
        Draws all renderables on screen 
        """
        pass
