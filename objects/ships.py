# Ships configuration
from objects.ship_bases import *


class Jet(BattleShip):
    MAX_HEALTH = 100
    MAX_ARMOR = 0
    DAMAGE = 10


class HeavyJet(BattleShip):
    MAX_HEALTH = 250
    MAX_ARMOR = 2
    DAMAGE = 18
    AT_SPEED = 1.5


class Cruiser(BattleShip, SupportShip):
    MAX_HEALTH = 1000
    MAX_ARMOR = 2
    DAMAGE = 30
    SHIELD = 10
    AT_SPEED = 2

    def __init__(self, *args):
        super().__init__(*args)

    def shoot(self, target):
        self.weapon.shoot(self, target, cd=5)


class CargoShip(TransportShip):
    MAX_HEALTH = 2000
    MAX_ARMOR = 0
    CARGO = 500


class RepairShip(SupportShip):
    MAX_HEALTH = 500
    MAX_ARMOR = 0
    TEAM = 15
