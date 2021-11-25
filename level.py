from pathlib import Path
from typing import List

from pygame import Rect

from interfaces import MapObject
from landscape import Brick, Steel, Grass, Water, Ice, Empty


class MapCreator:
    block_dict = {'B': Brick,
                  'S': Steel,
                  'W': Water,
                  'G': Grass,
                  'I': Ice,
                  'E': Empty}

    def __init__(self, level_number: int):
        levels_path = str(Path(Path.cwd(), 'Levels'))

    def create_map(self, tile_size=16) -> list:
        lvl_map: List[MapObject] = []
        with open(self.level_path, 'r') as lvl_data:
            for i, line in enumerate(lvl_data.readlines()):
                for j, symbol in enumerate(line):
                    pos = (j * tile_size, i * tile_size)
                    rect = Rect(pos, (tile_size, tile_size))
                    if symbol == '\n' or symbol == 'H':
                        continue
                    map_object = self.block_dict[symbol](rect)
                    lvl_map.append(map_object)
        return lvl_map


class Level:
    def __init__(self, level_number: int):
        self.map = MapCreator(level_number).create_map()