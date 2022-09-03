from objects.ships import *
from colorama import Fore, Style
import os
import asyncio

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
            return Fore.LIGHTBLACK_EX + '*' * 10 + '_' * 6 + '\\' * 8 + Style.RESET_ALL  # death string

    def screen(self):
        print('\n')
        # Team names
        print(self.teams[0].name + self.space(self.teams[0].name) + self.teams[1].name)
        # Team members
        for i in range(5):
            ship_1, ship_2 = self.teams[0].ships[i], self.teams[1].ships[i]
            string_1, string_2 = self.ship_field(ship_1), self.ship_field(ship_2)

            print(string_1 + self.space(string_1) + string_2)

    # Coroutines
    async def screen_coroutine(self):
        while self.running:
            self.clear_screen()
            self.screen()
            await asyncio.sleep(2.5)

    async def actions_coroutine(self, ship, team_enemy):
        while ship.health > 0 and self.running:
            if team_enemy.size > 0:
                ship.actions(team_enemy=team_enemy)
                await asyncio.sleep(ship.reload)
            else:
                self.endgame(ship.team)

    async def timer_coroutine(self):
        s = 0
        m = 0
        while s <= 60 and self.running:
            print(f'{m}:0{s}') if s < 10 else print(f'{m}:{s}')
            await asyncio.sleep(1)
            s += 1
            if s == 60:
                m += 1
                s = 0

    def endgame(self, winner):
        """Stops the game"""
        self.running = False
        self.clear_screen()
        print(f'\n{winner.name} is winner')
        self.screen()

    async def main(self):
        """Gathers all coroutines together"""
        screen_cr = asyncio.create_task(self.screen_coroutine())
        timer_cr = asyncio.create_task(self.timer_coroutine())
        coroutines = [screen_cr, timer_cr]
        for team in self.teams:
            enemy_team = self.teams[1] if team == self.teams[0] else self.teams[0]
            for ship in team.ships:
                actions_cr = asyncio.create_task(self.actions_coroutine(ship, enemy_team))
                coroutines.append(actions_cr)
        await asyncio.gather(*coroutines)


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    asyncio.run(btf.main())
