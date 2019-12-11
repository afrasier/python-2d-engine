import pygame
import abc
from abc import ABC, abstractmethod, abstractproperty
from interface import Position, ANCHORS

from typing import List


class Renderable(ABC):
    """
    Renderable object abstract base class to guarantee certain functionality on children
    """

    @abc.abstractproperty
    def surface(self) -> pygame.Surface:
        """
        Should return the renderable surface for blitting to the screen
        """
        raise NotImplementedError

    @abc.abstractproperty
    def position(self) -> Position:
        """
        Should return the renderable's position
        """
        raise NotImplementedError

    @abc.abstractproperty
    def anchor(self) -> ANCHORS:
        """
        Should return the "anchor" position for rendering
        i.e. If this renderables position is 50,50 and the anchor is TOP_LEFT, the top left
             most pixel of the renderable will be at 50,50
             If the anchor is CENTER, the center pixel will be at 50,50
        """
        return ANCHORS.TOP_LEFT
