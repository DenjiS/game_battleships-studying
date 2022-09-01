from objects.ship_modules import *
from colorama import Style
from random import random, choice
from time import sleep


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.CLS_NAME = name


class Ship(metaclass=ShipBuilder):
    def __init__(self, team, num):
        self.team = team
        self.num = num
        self.name = team.color + self.CLS_NAME + f'_{num}' + Style.RESET_ALL
        self.health = self.MAX_HEALTH
        self.armor = self.MAX_ARMOR

    def actions(self, team_enemy):
        if hasattr(self, 'weapon')
            targets = [i for i in team_enemy.ships if i is not None]
            enemy = choice(targets)
            self.take_enemy(enemy)
            sleep(0.5)

class BattleShip(Ship):
    HIT_CHANCE = 0.85

    def __init__(self, *args):
        super().__init__(*args)
        self.weapon = Weapon(self.DAMAGE)

    def shoot(self, target):
        self.weapon.shoot(self, target)

    def take_enemy(self, enemy):
        roll = random()
        if roll <= self.HIT_CHANCE:
            self.shoot(enemy)
        else:
            self.shoot(None)


class TransportShip(Ship):
    def __init__(self, *args):
        super().__init__(*args)
        self.storage = Storage(self.CARGO)


class SupportShip(Ship):
    SHIELD = None
    TEAM = None

    def __init__(self, *args):
        super().__init__(*args)
        if self.SHIELD:
            self.shield = Shield(self.SHIELD)
        if self.TEAM:
            self.repair_team = RepairTeam(self.TEAM)
