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
        self.cruiser1, self.cruiser2 = Cruiser(self.team1, 7), Cruiser(self.team2, 7)

    def test_has_repair_team(self):
        self.assertFalse(hasattr(self.cruiser1, 'repair_team'))
