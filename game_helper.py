from pathlib import Path
from pygame import Rect
from enemies import Common, Fast, RapidFire, Armored
from landscape import Brick, Steel, Grass, Water, Ice, Eagle


class MapCreator:
    block_dict = {'B': Brick,
                  'S': Steel,
                  'W': Water,
                  'G': Grass,
                  'I': Ice}

    def __init__(self, level_number: int):
        levels_path = str(Path(Path.cwd(), 'Levels'))
        self.level_path = levels_path + f'/{level_number}.txt'

    def create_map(self, tile_size=16) -> list:
        lvl_map = [Eagle()]
        with open(self.level_path, 'r') as lvl_data:
            for i, line in enumerate(lvl_data.readlines()):
                for j, symbol in enumerate(line):
                    pos = (j * tile_size, i * tile_size)
                    rect = Rect(pos, (tile_size, tile_size))
                    if symbol == '\n' or symbol == 'H' or symbol == '.':
                        continue
                    map_object = self.block_dict[symbol](rect)
                    lvl_map.append(map_object)
        return lvl_map


class EnemyQueueCreator:
    # noinspection PyTypeChecker
    enemies_queue = [18 * [Common] + 2 * [Fast],
                     2 * [Armored] + 4 * [Fast] + 14 * [Common],
                     14 * [Common] + 4 * [Fast] + 2 * [Armored],
                     10 * [RapidFire] + 5 * [Fast] + 2 * [Common] + 3 * [Armored],
                     5 * [RapidFire] + 2 * [Armored] + 8 * [Common] + 5 * [Fast]]

    def generate_queue(self, level_num: int):
        return self.enemies_queue[level_num - 1]


class GameHelper:
    queue_creator = EnemyQueueCreator()
    spawn_positions = [(192, 0), (384, 0), (0, 0)]
    spawn_index = 0

    def __init__(self, level_num):
        self.enemies_spawned = 0
        self.enemies_queue = self.queue_creator.generate_queue(level_num)

    def spawn_enemies(self, enemies):
        if len(enemies) > 3:
            return
        if len(self.enemies_queue) == 0:
            return
        self.enemies_spawned += 1
        is_bonus = False
        if self.enemies_spawned in [4, 8, 18]:
            is_bonus = True
        pos = self.spawn_positions[self.spawn_index]
        spawning_enemy = self.enemies_queue.pop(0)(pos, is_bonus)
        self.spawn_index = (self.spawn_index + 1) % 3
        enemies.append(spawning_enemy)
