from objects.ships import *
from adds import print_time_passed
from time import sleep
from colorama import Fore, Style
import os

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
    def space(cls, obj, length=65, symbol=' '):
        return symbol * (length - len(obj))

    def ship_field(self, ship):
        if ship:
            space_ship_field = self.space(ship.name, length=25, symbol='_')
            armor_bar, health_bar = f'AR:{ship.armor}', f'HP:{ship.health}\\{ship.MAX_HEALTH}'
            ship_bars = armor_bar + self.space(armor_bar, length=6) + health_bar
            return ship.name + space_ship_field + ship_bars
        elif not ship:
            return Fore.LIGHTBLACK_EX + '*' * 10 + '_' * 6 + '\\' * 16 + Style.RESET_ALL  # death string

    def screen(self):
        print('\n')
        # Team names
        team_str_1 = self.teams[0].name + self.space(self.teams[0].name, length=25) + 'stats'
        team_str_2 = self.teams[1].name + self.space(self.teams[1].name, length=25) + 'stats'
        print(team_str_1 + self.space(team_str_1) + team_str_2)
        # Team members
        for i in range(Team.SIZE):
            ship_1, ship_2 = self.teams[0].ships[i], self.teams[1].ships[i]
            string_1, string_2 = self.ship_field(ship_1), self.ship_field(ship_2)

            print(string_1 + self.space(string_1) + string_2)

    def battle_gen(self):
        cursor = 0
        while self.teams[0].size > 0 and self.teams[1].size > 0:
            num = int(cursor / 2)
            team = cursor % 2
            next_ship = self.teams[team].ships[num]
            if next_ship:
                enemy_team = self.teams[1] if next_ship.team == self.teams[0] else self.teams[0]
                yield next_ship, enemy_team
            else:
                yield None, None
            if cursor == 9:
                cursor = 0
            else:
                cursor += 1

    def endgame(self):
        self.running = False
        self.clear_screen()
        winner = self.teams[0] if any(self.teams[0].ships) else self.teams[1]
        print(f'\n{winner.name} is winner')
        self.screen()
        print('\nFINISH')

    @print_time_passed
    def mainloop(self):
        gen = self.battle_gen()
        while self.running:
            self.clear_screen()
            self.screen()
            sleep(0.5)
            try:
                ship, enemy_team = next(gen)
                if ship:
                    ship.actions(enemy_team)

            except StopIteration:
                self.endgame()


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.mainloop()
