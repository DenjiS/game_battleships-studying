from ship_modules import *


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        cls.name = name
        cls.health = Health(cls.MAX_HEALTH)
        cls.armor = cls.MAX_ARMOR


class Ship(metaclass=ShipBuilder):
    MAX_HEALTH = None
    MAX_ARMOR = None
    dead = False


class BattleShip(Ship):
    @property
    def weapon(self):
        return Weapon(dmg=self.DAMAGE)


class TransportShip(Ship):
    @property
    def storage(self):
        return Storage(cargo=self.CARGO)


class SupportShip(Ship):
    @property
    def shield(self):
        return Shield(shield=self.SHIELD)

    @property
    def rep_team(self):
        return RepairTeam(size=self.TEAM)
