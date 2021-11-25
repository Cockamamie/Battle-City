from pathlib import Path
from pygame import Rect
from landscape import Brick, Steel, Grass, Water, Ice
from interfaces import MapObject


class LevelCreator:
    block_dict = {'B': Brick,
                  'S': Steel,
                  'W': Water,
                  'G': Grass,
                  'I': Ice}

    def __init__(self, level_number: int):
        levels_path = str(Path(Path.cwd(), 'Levels'))
        self.level_path = levels_path + f'{level_number}.txt'

    def create_level(self, tile_size=32) -> list:
        lvl_map: list[MapObject] = []
        with open(self.level_path, 'r') as lvl_data:
            for i, line in enumerate(lvl_data.readlines()):
                for j, symbol in enumerate(line):
                    pos = (j * tile_size, i * tile_size)
                    rect = Rect(pos, tile_size, tile_size)
                    map_object = self.block_dict[symbol](rect)
                    lvl_map.append(map_object)
        return lvl_map


class Level:
    def __init__(self, level_number: int):
        self.map = LevelCreator(level_number).create_level()
