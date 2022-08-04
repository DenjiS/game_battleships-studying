from ship_modules import *
from colorama import Style


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        cls.name = name
        cls.health = Health(cls.MAX_HEALTH)
        cls.armor = cls.MAX_ARMOR


class Ship(metaclass=ShipBuilder):
    MAX_HEALTH = None
    MAX_ARMOR = None
    dead = False

    def __init__(self, team, num):
        self.name = team.color + self.name + f'_{num}' + Style.RESET_ALL


class BattleShip(Ship):
    @property
    def weapon(self):
        return Weapon(dmg=self.DAMAGE)

    def shoot(self, target=None):
        if target:
            target.health -= self.weapon.dmg
            print(f'{self.name} : shoot --> {target.name}')
            if target.dead:
                print(f'{target.name} destroyed')
        else:
            print(f'{self.hame} : shoot --> missed')


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
