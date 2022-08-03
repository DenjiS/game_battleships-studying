# Ships configuration
from ship_bases import *


class Jet(BattleShip):
    MAX_HEALTH = 100
    MAX_ARMOR = 0
    DAMAGE = 10


class HeavyJet(BattleShip):
    MAX_HEALTH = 250
    MAX_ARMOR = 2
    DAMAGE = 18


class Cruiser(BattleShip, SupportShip):
    MAX_HEALTH = 1000
    MAX_ARMOR = 2
    DAMAGE = 30
    SHIELD = 10


class CargoShip(TransportShip):
    MAX_HEALTH = 2000
    MAX_ARMOR = 0
    CARGO = 500


class RepairShip(SupportShip):
    MAX_HEALTH = 500
    MAX_ARMOR = 0
    TEAM = 15
