from objects.ship_modules import *
from colorama import Style
from random import random, choice
from abc import abstractmethod, ABC


class Ship(ABC):
    def __init__(self, team, num):
        self.team = team
        self.num = num
        self.name = team.color + self.__class__.__name__ + f'_{num}' + Style.RESET_ALL
        self.health = self.MAX_HEALTH
        self.armor = self.MAX_ARMOR
        self.reload = 0

    @abstractmethod
    def actions(self): self.reload = 0


# Ship Subtypes
class BattleShip(Ship):
    HIT_CHANCE = 0.85
    RELOAD = 2

    def __init__(self, *args):
        super().__init__(*args)
        self.weapon = Weapon(self.DAMAGE, self.RELOAD)

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

    def actions(self, team_enemy=None):
        super().actions()
        self.take_enemy(team_enemy)
        self.reload += self.weapon.reload


class SupportShip(Ship):
    SHIELD = None
    TEAM = None

    def __init__(self, *args):
        super().__init__(*args)
        if self.SHIELD:
            self.shield = Shield(self.SHIELD)
        if self.TEAM:
            self.repair_team = RepairTeam(self.TEAM)

    def team_buff(self):
        if self.shield.battery > 0:
            self.shield.team_buff(self)

    def actions(self, **kwargs):
        super().actions()
        if hasattr(self, 'shield'):
            self.team_buff()
            self.reload += self.shield.reload
        if hasattr(self, 'repair_team'):
            self.reload += self.repair_team.reload


class TransportShip(Ship):
    def __init__(self, *args):
        super().__init__(*args)
        self.storage = Storage(self.CARGO)

    def charge_ships(self):
        for ally in self.team.ships:
            if hasattr(ally, 'shield') and ally.shield.battery <= 0 and self.storage.cargo > ally.SHIELD:
                self.storage.charge_shield(ally)
                print(f'{self.name} : charging shield ({ally.SHIELD}) --> {ally.name}')

    def actions(self, **kwargs):
        super().actions()
        self.charge_ships()
        self.reload += self.storage.reload
