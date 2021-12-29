from Assets.sprites import SpritesCreator
from enums import Direction
from tank import Tank


class Player(Tank):
    def __init__(self):
        sprites_creator = SpritesCreator()
        images = sprites_creator.no_stars_player()
        super().__init__(direction=Direction.Up, is_player=True, images=images,
                         position=(144, 382))
