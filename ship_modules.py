# Battle modules
class Weapon:
    def __get__(self, obj, owner):
        return obj.DAMAGE


# Transport modules
class Storage:
    def __get__(self, obj, owner):
        return obj.CARGO


# Repair modules
class Shield:
    def __get__(self, obj, owner):
        return obj.SHIELD


class Team:
    def __get__(self, obj, owner):
        return obj.TEAM
