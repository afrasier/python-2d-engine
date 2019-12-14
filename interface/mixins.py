import pygame
from datetime import datetime
from abc import ABC, abstractmethod

from interface.renderable import Renderable
from interface import Position


class ClickAwareMixin(ABC):
    """
    ClickAwareMixin is a mixin which provides functions for handling "on click" events

    Mainly for use with renderable class, since it relies upon having a surface
    """

    def handle_click(self, event: pygame.event.Event) -> bool:
        """
        Function which takes a click event as a parameter, checks if the position falls within the object's surface
        If the click hits this item, call the internal child implementation for _handle_click

        Returns true or false if the click was handled by this object; allowing for differing event consumption.
        """
        if self.position_intersects(Position(*event.pos)):
            self._handle_click(event)
            return True
        return False

    @abstractmethod
    def position_intersects(self, position: Position) -> bool:
        """
        Should be implemented by the base class (if using renderable, ensure it comes last in resolution order)
        """
        raise NotImplementedError

    @property
    def clickable(self) -> bool:
        """
        Returns true, since all click awares are clickable
        """
        return True

    @abstractmethod
    def _handle_click(self, event: pygame.event.Event) -> None:
        """
        Handle a click event
        """
        raise NotImplementedError


class HoverAwareMixin(ABC):
    """
    HoverAwareMixin is a mixin which provides functions for handling "hover" events

    Mainly for use with renderable class, since it relies upon having a surface
    """

    def handle_mousemove(self, event: pygame.event.Event) -> bool:
        """
        Function which takes a mouse move event as a parameter, checks if the position falls within the object's surface
        If the mousemove is in the region, update the internal hover state

        Returns true or false if the click was handled by this object; allowing for differing event consumption.
        """
        intersect: bool = self.position_intersects(Position(*event.pos))
        if intersect and not self.is_hovered:
            self._is_hovered = True
            self._time_hovered = datetime.now()
            self._handle_hover(event, True)
            return True
        if not intersect and self.is_hovered:
            self._is_hovered = False
            self._handle_hover(event, False)
        return False

    @abstractmethod
    def position_intersects(self, position: Position) -> bool:
        """
        Should be implemented by the base class (if using renderable, ensure it comes last in resolution order)
         """
        raise NotImplementedError

    @property
    def hoverable(self) -> bool:
        """
        Returns true, since all click awares are clickable
        """
        return True

    @property
    def is_hovered(self) -> bool:
        """
        Returns true if is hovered, otherwise false
        """
        if not hasattr(self, "_is_hovered"):  # Why this? Name mangling
            self._is_hovered = False

        return self._is_hovered

    @property
    def time_hovered(self) -> datetime:
        """
        Returns the datetime of when this object was set to hovered. Returns None if it is not hovered
        """
        if self.is_hovered:
            return self._time_hovered
        else:
            return None

    def _handle_hover(self, event: pygame.event.Event, hover_state: bool) -> None:
        """
        Optional override. Adds a hook for doing something when hover state changes
        """
        pass
