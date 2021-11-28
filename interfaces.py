from abc import ABCMeta, abstractmethod
from pygame import Rect


class EnemyTank:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def health(self): pass

    @property
    @abstractmethod
    def velocity(self): pass

    @property
    @abstractmethod
    def shouting_speed(self): pass

    @property
    @abstractmethod
    def points(self): pass


class MapObject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, rect: Rect): pass
