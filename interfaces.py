from abc import ABCMeta, abstractmethod


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
    