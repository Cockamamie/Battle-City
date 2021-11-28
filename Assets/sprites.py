from pygame import image, Surface
from pathlib import Path
from enums import Direction, Color


class SpritesCreator:
    def __init__(self):
        self.assets_path = str(Path(Path.cwd(), 'Assets'))
        self.player = self.assets_path + '\\PlayerTank\\'
        self.second_player = self.assets_path + '\\SecondPlayerTank\\'
        self.power_ups = self.assets_path + '\\PowerUps\\'
        self.bullet_path = self.assets_path + '\\Bullet\\'
        self.blast = self.assets_path + '\\Blast\\'
        self.spawn = self.assets_path + '\\EnemySpawn\\'
        self.base = self.assets_path + '\\Base\\'
        self.__blocks = self.assets_path + '\\Blocks\\'

    def eagle(self):
        return image.load(f'{self.base}eagle.png').convert_alpha()

    def flag(self):
        return image.load(f'{self.base}flag.png').convert_alpha()

    @staticmethod
    def convert_dict_alpha(images: dict) -> dict[any, Surface]:
        for key in images.keys():
            images[key] = images[key].convert_alpha()
        return images

    def create_tank_dict(self, folder: str, img_prefix: str) -> dict[Direction, Surface]:
        return self.convert_dict_alpha(
            {Direction.Up: image.load(f'{folder}{img_prefix}_up.png'),
             Direction.Down: image.load(f'{folder}{img_prefix}_down.png'),
             Direction.Right: image.load(f'{folder}{img_prefix}_right.png'),
             Direction.Left: image.load(f'{folder}{img_prefix}_left.png')})

    def no_stars_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.player, 'no_stars')

    def one_star_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.player, 'one_star')

    def two_stars_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.player, 'two_stars')

    def three_stars_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.player, 'three_stars')

    def enemy_spawn(self) -> list[Surface]:
        return [image.load(f'{self.spawn}small.png').convert_alpha(),
                image.load(f'{self.spawn}medium.png').convert_alpha(),
                image.load(f'{self.spawn}large.png').convert_alpha(),
                image.load(f'{self.spawn}huge.png').convert_alpha()]

    def common_enemy(self, color: Color) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'common')

    def fast_enemy(self, color: Color) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'fast')

    def rapid_enemy(self, color: Color) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'rapid')

    def armored_enemy(self, color: Color) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.assets_path +
                                     f'\\{color.value}Tank\\', 'armored')

    def no_stars_second_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.second_player, 'no_stars')

    def one_star_second_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.second_player, 'one_star')

    def two_stars_second_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.second_player, 'two_stars')

    def three_stars_second_player(self) -> dict[Direction, Surface]:
        return self.create_tank_dict(self.second_player, 'three_stars')

    def bullet(self) -> dict[Direction, Surface]:
        return self.convert_dict_alpha(
            {Direction.Up: image.load(f'{self.bullet_path}up.png'),
             Direction.Down: image.load(f'{self.bullet_path}down.png'),
             Direction.Right: image.load(f'{self.bullet_path}right.png'),
             Direction.Left: image.load(f'{self.bullet_path}left.png')})

    def small_blast(self) -> Surface:
        return image.load(f'{self.blast}small.png').convert_alpha()

    def medium_blast(self) -> Surface:
        return image.load(f'{self.blast}medium.png').convert_alpha()

    def large_blast(self) -> Surface:
        return image.load(f'{self.blast}large.png').convert_alpha()

    def huge_blast(self) -> Surface:
        return image.load(f'{self.blast}huge.png').convert_alpha()

    def grenade(self) -> Surface:
        return image.load(f'{self.power_ups}grenade.png').convert_alpha()

    def health(self) -> Surface:
        return image.load(f'{self.power_ups}health.png').convert_alpha()

    def helmet(self) -> Surface:
        return image.load(f'{self.power_ups}helmet.png').convert_alpha()

    def helmet_effect(self) -> list[Surface]:
        return [image.load(f'{self.power_ups}helmet_effect_1.png').convert_alpha(),
                image.load(f'{self.power_ups}helmet_effect_2.png').convert_alpha()]

    def shovel(self) -> Surface:
        return image.load(f'{self.power_ups}shovel.png').convert_alpha()

    def star(self) -> Surface:
        return image.load(f'{self.power_ups}star.png').convert_alpha()

    def timer(self) -> Surface:
        return image.load(f'{self.power_ups}timer.png').convert_alpha()

    def brick(self) -> Surface:
        return image.load(f'{self.__blocks}brick.png').convert_alpha()

    def steel(self) -> Surface:
        return image.load(f'{self.__blocks}steel.png').convert_alpha()

    def grass(self) -> Surface:
        return image.load(f'{self.__blocks}grass.png').convert_alpha()

    def water(self) -> (Surface, Surface):
        return (image.load(f'{self.__blocks}water1.png').convert_alpha(),
                image.load(f'{self.__blocks}water2.png').convert_alpha())

    def ice(self) -> Surface:
        return image.load(f'{self.__blocks}ice.png').convert_alpha()
