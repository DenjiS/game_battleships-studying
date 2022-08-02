from ship_modules import Weapon, Storage, Shield, Team


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        cls.name = name
        cls.health = cls.MAX_HEALTH
        cls.armor = cls.MAX_ARMOR


class Ship(metaclass=ShipBuilder):
    MAX_HEALTH = None
    MAX_ARMOR = None


class BattleShip(Ship):
    weapon = Weapon()


class TransportShip(Ship):
    storage = Storage()


class SupportShip(Ship):
    shield = Shield()
    team = Team()
