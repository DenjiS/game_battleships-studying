from unittest import TestCase
from main import Team
from objects.ships import *
from colorama import Fore


def custom_log(string):
    return print(Fore.GREEN + string + Style.RESET_ALL)


class ShootTest(TestCase):
    def setUp(self):
        self.team1, self.team2 = Team('one', Fore.RED), Team('two', Fore.BLUE)
        self.jet1, self.jet2 = Jet(self.team1, 0), Jet(self.team2, 0)
        self.team1.ships[0], self.team2.ships[0] = self.jet1, self.jet2

    def test_shoot(self):
        custom_log('test_shoot')
        self.jet1.shoot(self.jet2)
        self.assertEqual(90, self.jet2.health)

    def test_kill(self):
        """Убийство удалением из команды"""
        shooter, target = self.team1.ships[0], self.team2.ships[0]
        shooter.armor, target.armor = 0, 0

        shots_needed = int(target.MAX_HEALTH / shooter.DAMAGE) + 1
        for i in range(shots_needed):
            shooter.shoot(target)
            expected_health = target.MAX_HEALTH - (shooter.DAMAGE * (i + 1))
            self.assertEqual(expected_health, target.health,
                             msg=f'{shooter.name} -> {target.name} target HP must be {expected_health} after {i + 1} shot')
        self.assertEqual(None, self.team2.ships[0],
                         msg=f'enemy ship must be deleted from enemy team list after {shots_needed} shots')

    def test_kill_all(self):
        """Убийства всеми возможными вариантами shooter/target"""
        custom_log('test_kill_all')
        ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]
        shooter_list = (i for i in ship_types_list if hasattr(i(self.team1, 0), 'weapon'))
        for shooter in shooter_list:
            custom_log(f'SHOOTER: {shooter.CLS_NAME}')
            for target in ship_types_list:
                self.team1.ships[0], self.team2.ships[0] = shooter(self.team1, 0), target(self.team2, 0)
                custom_log(self.team1.ships[0].CLS_NAME + ' ' + self.team2.ships[0].CLS_NAME)
                self.test_kill()


class CruiserTest(TestCase):
    def setUp(self):
        self.team1, self.team2 = Team('one', Fore.RED), Team('two', Fore.BLUE)
        self.cruiser1, self.cruiser2 = Cruiser(self.team1, 0), Cruiser(self.team2, 0)

    def test_has_repair_team(self):
        self.assertFalse(hasattr(self.cruiser1, 'repair_team'))

    def test_cruiser_weapon_ability(self):
        custom_log('test_cruiser_weapon_ability')
        self.assertEqual(2, self.cruiser2.armor, msg='initial armor of the enemy Cruiser must be 2')

        self.cruiser1.shoot(self.cruiser2)  # shot 1 : first use of ability
        self.assertEqual(1, self.cruiser2.armor, msg='after first hit armor must be reduced by 1')

        for i in range(5):  # shot 2-6 : ability cooldown
            self.cruiser1.shoot(self.cruiser2)
            self.assertEqual(1, self.cruiser2.armor)

        self.cruiser1.shoot(self.cruiser2)  # shot 7 : second use of ability
        self.assertEqual(0, self.cruiser2.armor, msg='after 1+5 hits ability must be reloaded')

        for i in range(5):  # shot 8-12 : ability cooldown
            self.cruiser1.shoot(self.cruiser2)
            self.assertEqual(0, self.cruiser2.armor)
