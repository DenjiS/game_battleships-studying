# Battle modules
class Weapon:
    def __init__(self, dmg=None):
        self.dmg = dmg

    def __get__(self, instance, owner):
        return self.dmg


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
