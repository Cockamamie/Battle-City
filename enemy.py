from interfaces import EnemyTank


class CommonTank(EnemyTank):

    @property
    def health(self): return 1

    @property
    def velocity(self): return 1

    @property
    def shouting_speed(self): return 1

    @property
    def points(self): return 100


class FastTank(EnemyTank):

    @property
    def health(self): return 1

    @property
    def velocity(self): return 3

    @property
    def shouting_speed(self): return 2

    @property
    def points(self): return 200


class RapidFireTank(EnemyTank):

    @property
    def health(self): return 1

    @property
    def velocity(self): return 2

    @property
    def shouting_speed(self): return 3

    @property
    def points(self): return 300


class ArmoredTank(EnemyTank):

    @property
    def health(self): return 4

    @property
    def velocity(self): return 2

    @property
    def shouting_speed(self): return 2

    @property
    def points(self): return 400
