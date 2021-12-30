from Assets.sprites import SpritesCreator
from enemy import Enemy
from enums import Color, MovingSpeed, ShootingSpeed

sprites_creator = SpritesCreator()


class Common(Enemy):
    def __init__(self, position, is_bonus):
        images = sprites_creator.common_enemy()
        bonus_images = sprites_creator.common_enemy(Color.Red)
        super().__init__(velocity=MovingSpeed.Slow.value, images=images, position=position,
                         bonus_images=bonus_images, is_bonus=is_bonus)

    @property
    def points(self): return 100

    def switch_sprite(self):
        self._bonus_index = (self._bonus_index + 1) % 2
        self.images = [sprites_creator.common_enemy(), self._bonus_images][self._bonus_index]


class Fast(Enemy):
    def __init__(self, position, is_bonus):
        images = sprites_creator.fast_enemy()
        bonus_images = sprites_creator.fast_enemy(Color.Red)
        super().__init__(velocity=MovingSpeed.Fast.value, images=images, position=position,
                         bonus_images=bonus_images, is_bonus=is_bonus)

    @property
    def points(self): return 200

    def switch_sprite(self):
        self._bonus_index = (self._bonus_index + 1) % 2
        self.images = [sprites_creator.fast_enemy(), self._bonus_images][self._bonus_index]


class RapidFire(Enemy):
    def __init__(self, position, is_bonus):
        images = sprites_creator.rapid_enemy()
        bonus_images = sprites_creator.rapid_enemy(Color.Red)
        super().__init__(shouting_speed=ShootingSpeed.Fast.value, images=images, position=position,
                         bonus_images=bonus_images, is_bonus=is_bonus)

    @property
    def points(self): return 300

    def switch_sprite(self):
        self._bonus_index = (self._bonus_index + 1) % 2
        self.images = [sprites_creator.rapid_enemy(), self._bonus_images][self._bonus_index]


class Armored(Enemy):
    def __init__(self, position, is_bonus):
        images = sprites_creator.armored_enemy(Color.Green)
        bonus_images = sprites_creator.armored_enemy(Color.Red)
        super().__init__(health=400, images=images, position=position,
                         bonus_images=bonus_images, is_bonus=is_bonus)

    @property
    def points(self): return 400

    def handle_sprite(self):
        if self.health == 300:
            self.images = sprites_creator.armored_enemy(Color.Beige)
        if self.health == 200:
            self.images = sprites_creator.armored_enemy(Color.Swamp)
        if self.images == 100:
            self.images = sprites_creator.armored_enemy(Color.Gray)

    def switch_sprite(self):
        self._bonus_index = (self._bonus_index + 1) % 2
        images = sprites_creator.armored_enemy(Color.Green)
        if self.health == 300:
            images = sprites_creator.armored_enemy(Color.Beige)
        if self.health == 200:
            images = sprites_creator.armored_enemy(Color.Swamp)
        if self.images == 100:
            images = sprites_creator.armored_enemy(Color.Gray)
        self.images = [images, self._bonus_images][self._bonus_index]

    def take_damage(self, explosion_queue, enemies, index):
        super().take_damage(explosion_queue, enemies, index)
        self.handle_sprite()
