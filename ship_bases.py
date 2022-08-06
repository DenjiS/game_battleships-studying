from ship_modules import *
from colorama import Style


class ShipBuilder(type):
    def __init__(cls, name, bases, attrs):
        cls.cls_name = name


class Ship(metaclass=ShipBuilder):
    def __init__(self, team, num):
        self.team = team
        self.num = num
        self.name = team.color + self.cls_name + f'_{num}' + Style.RESET_ALL
        self.health = self.MAX_HEALTH
        self.armor = self.MAX_ARMOR


class BattleShip(Ship):
    @property
    def weapon(self):
        return Weapon(dmg=self.DAMAGE)

    def shoot(self, target=None):
        if target:
            target.health = target.health - self.weapon.dmg
            print(f'{self.name} : shoot --> {target.name}')
            if target.health <= 0:
                print(f'{target.name} destroyed')
                target.team.ships[target.num] = None

        else:
            print(f'{self.name} : shoot --> missed')


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
