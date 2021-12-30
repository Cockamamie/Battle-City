from Assets.sprites import SpritesCreator
from enums import Direction, MovingSpeed, ShootingSpeed
from tank import Tank
from pygame import Rect
from sound import Sounds

sprites_creator = SpritesCreator()
sounds = Sounds()


class Player(Tank):

    start_pos = (128, 384)

    def __init__(self):
        images = sprites_creator.no_stars_player()
        self._stars = 0
        self._hp = 3
        self._is_steel_destroyable = False
        self.destroy_sound = sounds.destroy_player
        self.fire_sound = sounds.fire
        self.score = 0

        super().__init__(direction=Direction.Up, is_player=True,
                         images=images, position=self.start_pos)

    @property
    def hp(self):
        return self._hp

    def try_pickup_bonus(self, bonus, enemies, explosion_queue):
        player_rect = Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)
        intersecting = player_rect.colliderect(bonus.rect)
        if not intersecting:
            return False
        bonus.perform(self, enemies, explosion_queue)
        return True

    def fire(self, bullets):
        self.fire_sound.play()
        self.shoot(bullets, self._is_steel_destroyable)

    def upgrade(self):
        if self._stars == 4:
            return
        self._stars += 1
        if self._stars == 1:
            self.images = sprites_creator.one_star_player()
            self.shouting_speed = ShootingSpeed.Fast.value
        if self._stars == 2:
            self.max_bullets_available = 2
            self.images = sprites_creator.two_stars_player()
        if self._stars == 3:
            self.images = sprites_creator.three_stars_player()
            self._is_steel_destroyable = True

    def increase_hp(self):
        if self._hp < 3:
            self._hp += 1

    def decrease_hp(self):
        self._hp -= 1

    def set_start_params(self):
        self._position = self.start_pos
        self._direction = Direction.Up
        self._image = self.images[self.direction]

    def reset(self):
        self.destroy_sound.play()
        self.decrease_hp()
        if self._hp == 0:
            pass
        self._stars = 0
        self.shouting_speed = ShootingSpeed.Default.value
        self._velocity = MovingSpeed.Default.value
        self.max_bullets_available = 1
        self._is_steel_destroyable = False
        self.images = sprites_creator.no_stars_player()
        self.set_start_params()
