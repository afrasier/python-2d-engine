class Position:
    """
    Position represents a location on an x/y grid
    """

    __slots__ = ["x", "y"]

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
