from enum import Enum


class Direction(Enum):
    Up = (0, -1)
    Down = (0, 1)
    Right = (1, 0)
    Left = (-1, 0)
