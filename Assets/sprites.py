from pygame import image
from pathlib import Path
from directions import Direction
from enum import Enum


class Color(Enum):
    Beige = 'Beige'
    Gray = 'Gray'
    Green = 'Green'
    Red = 'Red'
    Swamp = 'Swamp'


class SpritesCreator:
    def __init__(self):
        self.assets_path = str(Path(Path.cwd(), 'Assets'))
        self.player = self.assets_path + '\\PlayerTank\\'
        self.second_player = self.assets_path + '\\SecondPlayerTank\\'
        self.power_ups = self.assets_path + '\\PowerUps\\'
        self.bullet = self.assets_path + '\\Bullet\\'
        self.blast = self.assets_path + '\\Blast\\'
        self.spawn = self.assets_path + '\\EnemySpawn\\'
        self.base = self.assets_path + '\\Base\\'

    def eagle(self):
        return image.load(f'{self.base}eagle.png')

    def flag(self):
        return image.load(f'{self.base}flag.png')

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

    def enemy_spawn(self):
        return [image.load(f'{self.spawn}small.png'),
                image.load(f'{self.spawn}medium.png'),
                image.load(f'{self.spawn}large.png'),
                image.load(f'{self.spawn}huge.png')]

    def common_enemy(self, color: Color) -> dict:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'common')

    def fast_enemy(self, color: Color) -> dict:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'fast')

    def rapid_enemy(self, color: Color) -> dict:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'rapid')

    def armored_enemy(self, color: Color) -> dict:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'armored')

    def no_stars_second_player(self) -> dict:
        return self.create_tank_dict(self.second_player, 'no_stars')

    def one_star_second_player(self) -> dict:
        return self.create_tank_dict(self.second_player, 'one_star')

    def two_stars_second_player(self) -> dict:
        return self.create_tank_dict(self.second_player, 'two_stars')

    def three_stars_second_player(self) -> dict:
        return self.create_tank_dict(self.second_player, 'three_stars')

    def bullet(self) -> dict:
        return {Direction.Up: image.load(f'{self.bullet}up.png'),
                Direction.Down: image.load(f'{self.bullet}down.png'),
                Direction.Right: image.load(f'{self.bullet}right.png'),
                Direction.Left: image.load(f'{self.bullet}left.png')}

    def small_blast(self):
        return image.load(f'{self.blast}small.png')

    def medium_blast(self):
        return image.load(f'{self.blast}medium.png')

    def large_blast(self):
        return image.load(f'{self.blast}large.png')

    def huge_blast(self):
        return image.load(f'{self.blast}huge.png')

    def grenade(self):
        return image.load(f'{self.power_ups}grenade.png')

    def health(self):
        return image.load(f'{self.power_ups}health.png')

    def helmet(self):
        return image.load(f'{self.power_ups}helmet.png')

    def helmet_effect(self) -> list:
        return [image.load(f'{self.power_ups}helmet_effect_1.png'),
                image.load(f'{self.power_ups}helmet_effect_2.png')]

    def shovel(self):
        return image.load(f'{self.power_ups}shovel.png')

    def star(self):
        return image.load(f'{self.power_ups}star.png')

    def timer(self):
        return image.load(f'{self.power_ups}timer.png')