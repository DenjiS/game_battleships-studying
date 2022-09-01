# Battle modules
class Weapon:
    def __init__(self, dmg):
        self.cd_count = 0
        self.dmg = dmg

    def shoot(self, ship, target, cd=10):
        if target:

            # Damage
            target.health = target.health - (self.dmg - target.armor)
            print(f'{ship.name} : shoot --> {target.name}')

            # Armor reduction -- ability
            if self.cd_count <= 0 and target.armor > 0:
                target.armor = target.armor - 1
                print(f'{ship.name} : break_armor --> {target.name}')
                self.cd_count = cd + 1  # ability cooldown

            # Kill
            if target.health <= 0:
                print(f'{target.name} destroyed')
                target.team.ships[target.num] = None

            # Miss
        else:
            print(f'{ship.name} : shoot --> missed')

        self.cd_count -= 1


# Support modules
class Shield:
    def __init__(self, shield):
        self.shield = shield

    def team_buff(self, ship):
        for ally in ship.team.ships:
            ally.armor += 1
            self.shield -= 1
        print(f'{ship.name} : team buff (.armor +1)')


class RepairTeam:
    def __init__(self, size):
        self.size = size


# Transport modules
class Storage:
    def __init__(self, cargo):
        self.cargo = cargo
        self.size = cargo

    def charge(self, module, amount):
        self.cargo -= amount
        module += amount
