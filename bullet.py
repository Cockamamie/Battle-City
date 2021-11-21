from directions import Direction


class Bullet:
    def __init__(self, belongs_player: bool):
        self._belongs_player = belongs_player

    @property
    def belongs_player(self):
        return self._belongs_player
