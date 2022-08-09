from unittest import TestCase
from main import Team
from ships import Jet, Cruiser
from colorama import Fore


class ShootTest(TestCase):
    def setUp(self):
        self.team1, self.team2 = Team('one', Fore.RED), Team('two', Fore.BLUE)
        self.jet1, self.jet2 = Jet(self.team1, 0), Jet(self.team2, 0)
        self.team1.ships[0], self.team2.ships[0] = self.jet1, self.jet2

    def test_shoot(self):
        self.jet1.shoot(self.jet2)
        self.assertEqual(90, self.jet2.health)

    def test_kill(self):
        # Убийство удалением из команды
        for i in range(10):
            self.jet1.shoot(self.jet2)
        self.assertEqual(None, self.team2.ships[0])


class CruiserTest(TestCase):
    def setUp(self):
        self.team1, self.team2 = Team('one', Fore.RED), Team('two', Fore.BLUE)
        self.cruiser1, self.cruiser2 = Cruiser(self.team1, 0), Cruiser(self.team2, 0)

    def test_has_repair_team(self):
        self.assertFalse(hasattr(self.cruiser1, 'repair_team'))

    def test_weapon_ability(self):
        self.assertEqual(2, self.cruiser2.armor, msg='initial armor of the enemy Cruiser must be 2')

        self.cruiser1.shoot(self.cruiser2)  # shoot 1 : first use of ability
        self.assertEqual(1, self.cruiser2.armor, msg='after first hit armor must be reduced by 1')

        for i in range(5):   # shoot 2-6 : ability cooldown
            self.cruiser1.shoot(self.cruiser2)
            self.assertEqual(1, self.cruiser2.armor)

        self.cruiser1.shoot(self.cruiser2)   # shoot 6 : second use of ability
        self.assertEqual(0, self.cruiser2.armor, msg='after 5 hits ability must be reloaded')
