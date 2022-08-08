from ship_modules import *
from colorama import Style


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.cls_name = name


class Ship(metaclass=ShipBuilder):
    def __init__(self, team, num):
        self.team = team
        self.num = num
        self.name = team.color + self.cls_name + f'_{num}' + Style.RESET_ALL
        self.health = self.MAX_HEALTH
        self.armor = self.MAX_ARMOR


class BattleShip(Ship):
    def __init__(self, *args):
        super().__init__(*args)
        self.weapon = Weapon(dmg=self.DAMAGE)

    def shoot(self, target=None):
        self.weapon.shoot(self, target)


class TransportShip(Ship):
    def __init__(self, *args):
        super().__init__(*args)
        self.storage = Storage(cargo=self.CARGO)


class SupportShip(Ship):
    SHIELD = None
    TEAM = None

    def __init__(self, *args):
        super().__init__(*args)
        if self.SHIELD:
            self.shield = Shield(shield=self.SHIELD)
        if self.TEAM:
            self.repair_team = RepairTeam(size=self.TEAM)
