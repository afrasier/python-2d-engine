import pygame

from interface import Position
from interface.renderable import Renderable
from interface.mixins import ClickAwareMixin, HoverAwareMixin

from typing import Dict, List, Tuple, Union

TYPE_RENDERABLE: Union = Union[Renderable, ClickAwareMixin, HoverAwareMixin]


class Layer:
    """
    Layer represents an individual layer of renderables
    """

    def __init__(self, motion_scale: Tuple[float, float] = (1, 1)):
        # Scales the motion of the camera (useful for parallax or static items (scale = 0))
        self.motion_scale: Tuple[float, float] = motion_scale
        # Dictionary of renderables organized by id (dictionaries maintain their order in Python 3.6)
        self.renderables: Dict[int, TYPE_RENDERABLE] = {}

    def mouse_event_dispersal(self, event: pygame.event.Event) -> None:
        """
        Disperse mouse events to renderables
        """
        if event.type == pygame.MOUSEBUTTONUP:
            renderable: TYPE_RENDERABLE
            for renderable in self.renderables.values():
                if isinstance(renderable, ClickAwareMixin) and renderable.handle_click(event):
                    # Click was successful, so consume and move on
                    return
        elif event.type == pygame.MOUSEMOTION:
            found_new_hover: bool = False
            renderable: TYPE_RENDERABLE
            for renderable in self.renderables.values():
                if isinstance(renderable, HoverAwareMixin):
                    if not found_new_hover and renderable.handle_mousemove(event):
                        # Set found new hover to true
                        found_new_hover = True
                    elif found_new_hover and renderable.is_hovered:
                        # Only evaluate those who currently think they are hovered, so they can clear that state
                        renderable.handle_mousemove(event)

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

    def get_renderable_position(self, viewport_position: Position, renderable: Renderable) -> Tuple[float, float]:
        """
        Calculates a renderable's position on the screen based upon viewport position and layer scaling
        """
        anchored_position = renderable.anchored_position

        return (
            anchored_position.x - (viewport_position.x * self.motion_scale[0]),
            anchored_position.y - (viewport_position.y * self.motion_scale[1]),
        )

    def blit(self, viewport_position: Position, surface: pygame.Surface) -> None:
        """
        Renders this layer's renderables onto the given surface
        """
        for renderable in self.renderables.values():
            rendering_position = self.get_renderable_position(viewport_position, renderable)

            # Since this rendering position would mark the top left of the renderable, we can do a quick
            # check to see if the rendering position > surface width/height
            if rendering_position[0] > surface.get_width() or rendering_position[1] > surface.get_height():
                continue

            surface.blit(renderable.surface, rendering_position)


class Viewport:
    """
    viewport.py

    Represents a viewport; all items wishing to be rendered should be registered with this class via a layer

    Items are rendered based upon their layer, in the order they were added to that layer

    Priority is such that 0 is rendered on top of 1, and so on
    """

    def __init__(self):
        self.position: Position = Position()
        self.layers: Dict[int, Layer] = {}
        self.ordered_priorities: List[int] = []
        self.active = False

    def mouse_event_dispersal(self, event: pygame.event.Event) -> None:
        """
        Distributes mouse events to all layers, if this is an active viewport
        """
        if self.active:
            for layer in self.layers.values():
                layer.mouse_event_dispersal(event)

    def add_layer(self, priority: int, layer: Layer) -> bool:
        """
        Adds a layer to this viewport, returns true if the layer was successfully added
        """
        if priority not in self.layers:
            self.layers[priority] = layer
            self.__update_priorities()
            return True

        return False

    def remove_layer(self, priority: int = None, layer: Layer = None) -> None:
        """
        Removes a layer either by priority or by layer
        """
        if priority and priority in self.layers:
            del self.layers[priority]
        elif layer:
            try:
                # Quick-delete by value: look up value index in value list and delete key at that index in key list
                index = list(self.layers.values()).index(layer)
                del self.layers[list(self.layers.keys())[index]]
                self.__update_priorities()
            except ValueError:
                # This layer isn't in this viewport
                return

    def __update_priorities(self) -> None:
        """
        Updates the ordered priority list
        """
        self.ordered_priorities = sorted(list(self.layers.keys()), reverse=True)

    def blit(self, surface: pygame.Surface) -> None:
        """
        Draws all layers on screen 
        """
        for priority in self.ordered_priorities:
            self.layers[priority].blit(self.position, surface)
