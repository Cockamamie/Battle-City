from Assets.sprites import SpritesCreator
from enums import Direction, MovingSpeed, ShootingSpeed
from tank import Tank
from pygame import Rect
import power_ups

sprites_creator = SpritesCreator()


class Player(Tank):
    def __init__(self):
        images = sprites_creator.no_stars_player()
        self._stars = 0
        self._hp = 3
        self._is_steel_destroyable = False

        super().__init__(direction=Direction.Up, is_player=True,
                         images=images, position=(144, 382))

    def try_pickup_bonus(self, bonus: power_ups.PowerUp, enemies):
        player_rect = Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)
        intersecting = player_rect.colliderect(bonus.rect)
        if not intersecting:
            return False
        bonus.perform(self, enemies)
        return True

    def fire(self, bullets):
        self.shoot(bullets, self._is_steel_destroyable)

    def upgrade(self):
        if self._stars == 4:
            return
        self._stars += 1
        if self._stars == 1:
            self.images = sprites_creator.one_star_player()
        if self._stars == 2:
            self.images = sprites_creator.two_stars_player()
        if self._stars == 3:
            self.images = sprites_creator.three_stars_player()
            self._is_steel_destroyable = True

    def increase_hp(self):
        self._hp += 1

    def decrease_hp(self):
        self._hp -= 1
