from pygame import image
from pathlib import Path
from directions import Direction


class SpritesCreator:
    def __init__(self):
        self.assets_path = str(Path(Path.cwd(), ''))
        self.player = self.assets_path + '\\PlayerTanks\\'
        self.enemy = self.assets_path + '\\EnemyTanks\\'
        self.power_ups = self.assets_path + '\\PowerUps\\'

    @staticmethod
    def create_tank_dict(folder: str, img_prefix: str) -> dict:
        return {Direction.Up: image.load(f'{folder}{img_prefix}_up.png'),
                Direction.Down: image.load(f'{folder}{img_prefix}_down.png'),
                Direction.Right: image.load(f'{folder}{img_prefix}_right.png'),
                Direction.Left: image.load(f'{folder}{img_prefix}_left.png')}

    def no_stars_player(self) -> dict:
        return self.create_tank_dict(self.player, 'no_stars')

    def one_star_player(self) -> dict:
        return self.create_tank_dict(self.player, 'one_star')

    def two_stars_player(self) -> dict:
        return self.create_tank_dict(self.player, 'two_stars')

    def three_stars_player(self) -> dict:
        return self.create_tank_dict(self.player, 'three_stars')
