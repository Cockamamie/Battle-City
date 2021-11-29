from Assets.sprites import SpritesCreator
from enemy import Enemy

sprites_creator = SpritesCreator()


class Common(Enemy):
    def __init__(self, is_bonus: bool = False):
        images = sprites_creator.common_enemy()
        super().__init__(velocity=1, images=images)

    @property
    def points(self): return 100


class Fast(Enemy):
    def __init__(self, is_bonus: bool = False):
        images = sprites_creator.fast_enemy()
        super().__init__(velocity=3, images=images)

    @property
    def points(self): return 200


class RapidFire(Enemy):
    def __init__(self, is_bonus: bool = False):
        images = sprites_creator.rapid_enemy()
        super().__init__(shouting_speed=3, images=images)

    @property
    def points(self): return 300


class Armored(Enemy):
    def __init__(self, is_bonus: bool = False):
        images = sprites_creator.armored_enemy()
        super().__init__(health=400, images=images)

    @property
    def points(self): return 400
