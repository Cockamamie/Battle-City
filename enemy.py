from tank import Tank


class CommonTank(Tank):
    def __init__(self, is_bonus: bool = False):
        super().__init__(velocity=1)

    @property
    def points(self): return 100


class FastTank(Tank):
    def __init__(self, is_bonus: bool = False):
        super().__init__(velocity=3)

    @property
    def points(self): return 200


class RapidFireTank(Tank):
    def __init__(self, is_bonus: bool = False):
        super().__init__(shouting_speed=3)

    @property
    def points(self): return 300


class ArmoredTank(Tank):
    def __init__(self, is_bonus: bool = False):
        super().__init__(health=400)

    @property
    def points(self): return 400
