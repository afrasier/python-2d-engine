class Position:
    """
    Position represents a location on an x/y grid
    """

    __slots__ = ["x", "y"]

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def shift(self, x: float = 0, y: float = 0) -> None:
        """
        Shifts the point by a specified amount in x, y
        """
        self.x = self.x + x
        self.y = self.y + y

    def shifted(self, x: float = 0, y: float = 0) -> "Position":
        """
        Returns a copy of this position shifted by a specified amount in x, y
        """
        return Position(self.x + x, self.y + y)

    def __str__(self) -> str:  # pragma: no cover
        """
        Returns the string representation of the position
        """
        return f"({self.x}, {self.y})"
