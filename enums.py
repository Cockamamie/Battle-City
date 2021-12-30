from enum import Enum


class Color(Enum):
    Beige = 'Beige'
    Gray = 'Gray'
    Green = 'Green'
    Red = 'Red'
    Swamp = 'Swamp'


class Direction(Enum):
    Up = (0, -1)
    Down = (0, 1)
    Right = (1, 0)
    Left = (-1, 0)


class ShootingSpeed(Enum):
    Default = 6
    Fast = 9


class MovingSpeed(Enum):
    Slow = 1
    Default = 2
    Fast = 3
