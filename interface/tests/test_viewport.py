import pygame

from interface import Viewport, Position, Layer
from interface.renderable import Renderable


class MockSurface:
    def __init__(self, expected):
        self.expected = expected

    def blit(self, surface, location):
        assert location == self.expected

    def get_width(self):
        return 100

    def get_height(self):
        return 100


class DemoRenderable(Renderable):
    def __init__(self, f):
        self.f = f
        self._position = Position()

    @property
    def surface(self):
        return self.f

    @property
    def position(self):
        return self._position


def test_layer_add_remove():
    layer: Layer = Layer()

    dr = DemoRenderable(None)

    assert len(layer.renderables) == 0
    layer.add_renderable(dr)
    assert len(layer.renderables) == 1
    layer.remove_renderable(dr)
    assert len(layer.renderables) == 0


def test_layer_scaling():
    layer: Layer = Layer(motion_scale=(2, -2))
    dr = DemoRenderable(pygame.surface.Surface((10, 10)))

    ms = MockSurface((-10, 10))

    layer.add_renderable(dr)
    layer.blit(Position(5, 5), ms)


def test_viewport():
    vp = Viewport()

    layer: Layer = Layer(motion_scale=(2, -2))
    dr = DemoRenderable(pygame.surface.Surface((10, 10)))

    ms = MockSurface((-10, 10))

    layer.add_renderable(dr)

    vp.position.shift(5, 5)
    assert vp.add_layer(1, layer)
    assert len(vp.layers) == 1
    # Try adding same layer again to same priority
    assert not vp.add_layer(1, layer)

    # Try removing layers by priority
    vp.remove_layer(priority=1)
    assert len(vp.layers) == 0

    # Try removing this layer when it isn't in there
    vp.remove_layer(layer=layer)

    # Try adding the layer then removing it again
    vp.add_layer(5, layer)
    assert len(vp.layers) == 1
    vp.remove_layer(layer=layer)
    assert len(vp.layers) == 0

    # Try blitting
    vp.add_layer(5, layer)
    vp.blit(ms)

