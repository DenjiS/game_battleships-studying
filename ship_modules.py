# Battle modules
class Weapon:
    def __init__(self, dmg=None):
        self.cd_count = 0
        self.dmg = dmg

    def shoot(self, ship, target):
        if target:
            # Armor reduction ability
            if self.cd_count <= 0 and target.armor > 0:
                target.armor = target.armor - 1
                print(f'{ship.name} : break_armor --> {target.name}')
                self.cd_count = 10

            # Damage
            target.health = target.health - (self.dmg - target.armor)
            print(f'{ship.name} : shoot --> {target.name}')

            # Kill
            if target.health <= 0:
                print(f'{target.name} destroyed')
                target.team.ships[target.num] = None

        else:
            print(f'{ship.name} : shoot --> missed')

        self.cd_count -= 1


# Transport modules
class Storage:
    def __init__(self, cargo=None):
        self.cargo = cargo
        self.size = cargo


# Support modules
class Shield:
    def __init__(self, shield=None):
        self.shield = shield


class RepairTeam:
    def __init__(self, size=None):
        self.size = size
