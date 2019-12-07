import pygame
import abc
from abc import ABC, abstractmethod, abstractproperty
from interface import Position


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
