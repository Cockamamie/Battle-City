from pygame import mixer
from pathlib import Path


class Sounds:
    def __init__(self):
        mixer.init()
        self.sounds_path = str(Path(Path.cwd(), 'Assets')) + '/SoundEffects/'
        self.fire = mixer.Sound(self.sounds_path + 'shoot.wav')
        self.brick = mixer.Sound(self.sounds_path + 'hit_brick.wav')
        self.steel = mixer.Sound(self.sounds_path + 'hit_steel.wav')
        self.armor = mixer.Sound(self.sounds_path + 'hit_armor.wav')
        self.destroy_player = mixer.Sound(self.sounds_path + 'destroy_player.wav')
        self.destroy_eagle = mixer.Sound(self.sounds_path + 'destroy_eagle.wav')
        self.destroy_enemy = mixer.Sound(self.sounds_path + 'destroy_enemy.wav')
        self.hp_bonus = mixer.Sound(self.sounds_path + 'hp_bonus.wav')
        self.grenade_bonus = mixer.Sound(self.sounds_path + 'grenade_bonus.wav')
        self.star_bonus = mixer.Sound(self.sounds_path + 'star_bonus.wav')
        self.bonus_appears = mixer.Sound(self.sounds_path + 'bonus_appears.wav')
