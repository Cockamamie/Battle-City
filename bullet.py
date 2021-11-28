from enums import Direction
from Assets.sprites import SpritesCreator


class Bullet:
    def __init__(self, direction: Direction, start_position: (int, int),
                 owner,
                 belongs_player=False, is_steel_destroyable=False):
        self.__direction = direction
        self.__position = start_position
        self.velocity = 5
        self.__owner = owner
        self.__belongs_player = belongs_player
        self.__is_steel_destroyable = is_steel_destroyable

        sprites_creator = SpritesCreator()
        self.image = sprites_creator.bullet()[direction]
        self.rect = self.image.get_rect()
        self.blasts = [sprites_creator.small_blast(),
                       sprites_creator.medium_blast()]

    @property
    def direction(self): return self.__direction

    @property
    def position(self): return self.__position

    @property
    def owner(self): return self.__owner

    # @property
    # def velocity(self): return self.velocity

    @property
    def belongs_player(self): return self.__belongs_player

    @property
    def is_steel_destroyable(self): return self.__is_steel_destroyable

    def move(self):
        delta_pos = [delta * self.velocity for delta in self.direction.value]
        self.__position = tuple([x + y for x, y in zip(self.position, delta_pos)])
