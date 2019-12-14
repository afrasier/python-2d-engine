import pygame
from abc import ABC, abstractmethod, abstractproperty
from interface import Position, Anchor

from typing import List


class Renderable(ABC):
    """
    Renderable object abstract base class to guarantee certain functionality on children
    """

    @abstractproperty
    def surface(self) -> pygame.Surface:
        """
        Should return the renderable surface for blitting to the screen
        """
        raise NotImplementedError

    @abstractproperty
    def position(self) -> Position:
        """
        Should return the renderable's position
        """
        raise NotImplementedError

    @property
    def anchor(self) -> Anchor:
        """
        Should return the "Anchor" position for rendering
        i.e. If this renderables position is 50,50 and the Anchor is TOP_LEFT, the top left
             most pixel of the renderable will be at 50,50
             If the Anchor is CENTER, the center pixel will be at 50,50
        """
        return Anchor.TOP_LEFT

    @property
    def anchored_position(self) -> Position:
        """
        Returns the position, with appropriate Anchoring offset
        """
        width = self.surface.get_width()
        height = self.surface.get_height()
        half_width = width / 2
        half_height = height / 2

        anchor_offset = (0, 0)

        # Most used first for optimization
        if self.anchor == Anchor.BOTTOM_CENTER:
            anchor_offset = (half_width, height)
        elif self.anchor == Anchor.CENTER:
            anchor_offset = (half_width, half_height)
        elif self.anchor == Anchor.TOP_CENTER:
            anchor_offset = (half_width, 0)
        elif self.anchor == Anchor.CENTER_LEFT:
            anchor_offset = (0, half_height)
        elif self.anchor == Anchor.CENTER_RIGHT:
            anchor_offset = (width, half_height)
        elif self.anchor == Anchor.TOP_RIGHT:
            anchor_offset = (width, 0)
        elif self.anchor == Anchor.BOTTOM_LEFT:
            anchor_offset = (0, height)
        elif self.anchor == Anchor.BOTTOM_RIGHT:
            anchor_offset = (width, height)

        return self.position.shifted(-anchor_offset[0], -anchor_offset[1])

    def position_intersects(self, position: Position) -> bool:
        """
        Returns true if the supplied position intersects with this renderable's surface
        """
        top_left = self.anchored_position
        bottom_right = top_left.shifted(self.surface.get_width(), self.surface.get_height())

        return (
            position.x >= top_left.x
            and position.x <= bottom_right.x
            and position.y >= top_left.y
            and position.y <= bottom_right.y
        )
