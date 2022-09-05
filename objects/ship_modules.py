# Base modules
class Health:
    def __set__(self, instance, value):
        if value <= 0:  # death of the ship
            instance._health = 0
            instance.team.ships[instance.num] = None
            instance.team.size -= 1
            print(f'{instance.name} destroyed')
        else:
            instance._health = value

    def __get__(self, instance, owner):
        return instance._health


# Battle modules
class Weapon:
    def __init__(self, dmg):
        self.cd_count = 0
        self.dmg = dmg

    def shoot(self, ship, target, cd=5):
        if target:

            # Damage
            target.health -= (self.dmg - target.armor)
            print(f'{ship.name} : shoot --> {target.name}')

            # Armor reduction -- ability
            if self.cd_count <= 0 and target.armor > 0:
                target.armor = target.armor - 1
                print(f'{ship.name} : break_armor --> {target.name}')
                self.cd_count = cd + 1  # ability cooldown

            # Miss
        else:
            print(f'{ship.name} : shoot --> missed')

        self.cd_count -= 1


# Support modules
class Shield:
    def __init__(self, shield):
        self.battery = shield
        self.cd_count = 0

    def team_buff(self, ship):
        if self.cd_count <= 0 and self.battery > 0:
            for ally in ship.team.ships:
                if ally:
                    ally.armor += 1
            self.battery -= 1
            print(f'{ship.name} : team buff (.armor +1), bat={self.battery}')
            self.cd_count = 3
        else:
            self.cd_count -= 1


class RepairTeam:
    def __init__(self, size):
        self.size = size


# Transport modules
class Storage:
    def __init__(self, cargo):
        self.cargo = cargo

    def charge_shield(self, target):
        if self.cargo > target.SHIELD:
            self.cargo -= target.SHIELD
            target.shield.battery += target.SHIELD
