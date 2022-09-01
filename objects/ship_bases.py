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
        self.map = {}

    def actions(self, team_enemy):
        for module in self.map:
            self.map[module](team_enemy)


# Ship Subtypes
class BattleShip(Ship):
    HIT_CHANCE = 0.85

    def __init__(self, *args):
        super().__init__(*args)
        self.weapon = Weapon(self.DAMAGE)
        self.map[self.weapon] = self.take_enemy

    def shoot(self, target):
        self.weapon.shoot(self, target)

    def take_enemy(self, team_enemy):
        targets = [i for i in team_enemy.ships if i is not None]
        if targets:
            enemy = choice(targets)
            roll = random()
            if roll <= self.HIT_CHANCE:
                self.shoot(enemy)
            else:
                self.shoot(None)


class SupportShip(Ship):
    SHIELD = None
    TEAM = None

    def __init__(self, *args):
        super().__init__(*args)
        if self.SHIELD:
            self.shield = Shield(self.SHIELD)
            self.map[self.shield] = self.team_buff
        if self.TEAM:
            self.repair_team = RepairTeam(self.TEAM)

    def team_buff(self, *args):
        if self.shield.battery > 0:
            self.shield.team_buff(self)


class TransportShip(Ship):
    def __init__(self, *args):
        super().__init__(*args)
        self.storage = Storage(self.CARGO)
        self.map[self.storage] = self.charge_ships

    def charge_ships(self, *args):
        for ship in self.team.ships:
            if hasattr(ship, 'shield') and ship.shield.battery <= 0:
                self.storage.charge(ship.shield.battery, ship.SHIELD)
                print(f'{self.name} : charging shield ({ship.SHIELD}) --> {ship.name}')