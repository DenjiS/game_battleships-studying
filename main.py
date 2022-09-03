from objects.ships import *
from colorama import Fore, Style
import os
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    SIZE = 5

    def __init__(self, name, color):
        self.color = color
        self.name = color + name + Style.RESET_ALL
        self.size = self.SIZE

        self.ships = []
        # Ships initialization
        for num in range(self.SIZE):
            append_ship = choice(ship_types_list)(self, num)
            self.ships.append(append_ship)


class Battlefield:
    def __init__(self, *teams):
        self.teams = teams
        self.running = True

    # Methods used in Battlefield.screen()
    @classmethod
    def clear_screen(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def space(cls, obj):
        return ' ' * (65 - len(obj))

    @classmethod
    def ship_field(cls, ship):
        if ship:
            space_ship_field = 25 - len(ship.name)
            ship_bars = f'AR:{ship.armor}_HP:{ship.health}\\{ship.MAX_HEALTH}'
            return ship.name + '_' * space_ship_field + ship_bars
        elif not ship:
            return Fore.LIGHTBLACK_EX + '*' * 10 + '_' * 6 + '\\' * 8 + Style.RESET_ALL  # Death string

    def screen(self):
        print('\n')
        # Team names
        print(self.teams[0].name + self.space(self.teams[0].name) + self.teams[1].name)
        # Team members
        for i in range(5):
            ship_1, ship_2 = self.teams[0].ships[i], self.teams[1].ships[i]
            string_1, string_2 = self.ship_field(ship_1), self.ship_field(ship_2)

            print(string_1 + self.space(string_1) + string_2)

    # Threads
    def screen_thread(self):
        while self.running:
            self.screen()
            sleep(2.5)

    def actions_thread(self, ship, team_enemy):
        while ship.health > 0 and self.running:
            if team_enemy.size > 0:
                ship.actions(team_enemy=team_enemy)
                sleep(ship.reload)
            else:
                self.endgame(ship.team)

    def timer_thread(self):
        s = 0
        m = 0
        while s <= 60 and self.running:
            print(f'{m}:0{s}') if s < 10 else print(f'{m}:{s}')
            sleep(1)
            s += 1
            if s == 60:
                m += 1
                s = 0

    def endgame(self, winner):
        self.running = False
        self.clear_screen()
        print(f'\n{winner.name} is winner')
        self.screen()

    def main(self):
        with ThreadPoolExecutor(max_workers=12) as ex:
            ex.submit(self.screen_thread)
            ex.submit(self.timer_thread)
            for team in self.teams:
                team_enemy = self.teams[1] if team == self.teams[0] else self.teams[0]
                for ship in team.ships:
                    ex.submit(self.actions_thread, ship, team_enemy)


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.main()
