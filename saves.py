import shelve
from game_helper import GameHelper
from landscape import Eagle


def save(player, enemies, game_helper, bullets, obstacles, bonus):
    with shelve.open('Saves/save') as sh:
        sh['player'] = PlayerSave(player)
        save_enemies = []
        for enemy in enemies:
            save_enemies.append(EnemySave(enemy))
        sh['enemies'] = save_enemies
        sh['gh'] = GameHelperSave(game_helper)
        sh['bonus'] = BonusSave(bonus)
        save_obstacles = []
        for obstacle in obstacles:
            if isinstance(obstacle, Eagle):
                continue
            save_obstacles.append(ObstacleSave(obstacle))
        sh['obstacles'] = save_obstacles


def load(player, enemies, bullets, obstacles, medium):
    with shelve.open('Saves/save') as sh:
        player.set_from_save(sh['player'])

        enemies.clear()
        for e in sh['enemies']:
            enemy = e.enemy_class(e.position, e.is_bonus)
            enemy.set_from_save(e)
            enemies.append(enemy)

        game_helper = GameHelper(0)
        game_helper.set_from_save(sh['gh'])

        b = sh['bonus']
        if b.bonus_class is None.__class__:
            bonus = None
        else:
            bonus = b.bonus_class(b.position)
            bonus.set_from_save(b)

        obstacles.clear()
        medium.empty()
        eagle = Eagle()
        obstacles.append(eagle)
        medium.add(eagle)
        for obs in sh['obstacles']:
            obstacle = obs.obstacle_class(obs.rect)
            obstacles.append(obstacle)
            medium.add(obstacle)

        return game_helper, bonus


class PlayerSave:
    def __init__(self, player):
        self.health = player.health
        self.velocity = player.velocity
        self.shouting_speed = player.shouting_speed
        self.direction = player.direction
        self.position = player.position
        self.max_bullets_available = player.max_bullets_available
        self.stars = player.stars
        self.hp = player.hp
        self.is_steel_destroyable = player.is_steel_destroyable
        self.score = player.score


class EnemySave:
    def __init__(self, enemy):
        self.health = enemy.health
        self.direction = enemy.direction
        self.position = enemy.position
        self.max_bullets_available = enemy.max_bullets_available
        self.is_bonus = enemy.is_bonus
        self.bonus_index = enemy.bonus_index
        self.timer = enemy.timer
        self.enemy_class = enemy.__class__


class GameHelperSave:
    def __init__(self, gh):
        self.spawn_index = gh.spawn_index
        self.enemies_spawned = gh.enemies_spawned
        self.enemies_queue = gh.enemies_queue


class BonusSave:
    def __init__(self, bonus):
        self.bonus_class = bonus.__class__
        if bonus is None:
            return
        self.position = bonus.position
        self.rect = bonus.rect
        self.is_visible = bonus.is_visible


class ObstacleSave:
    def __init__(self, obs):
        self.rect = obs.rect
        self.obstacle_class = obs.__class__
