from objects.ships import *
from random import choice
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

        self.ships = []
        for num in range(self.SIZE):
            # Создание объекта корабля
            append_ship = choice(ship_types_list)(self, num)
            self.ships.append(append_ship)


class Battlefield:
    def __init__(self, team_1, team_2):
        # Инициализация команд
        self.teams = team_1, team_2
        self.running = True

    @classmethod
    def clear_screen(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def space(cls, obj):
        """Метод для формирования ровной колонки правой команды при отображении Battlefield.screen;
        :param obj: str - текст левой команды
        :return: str - необходимое кол-во пробелов перед текстом правой команды
        """
        return ' ' * (65 - len(obj))

    @classmethod
    def ship_field(cls, ship):
        """Поле корабля для Battlefield.screen;
        :param ship: obj - объект корабля
        :return: str - название, здоровье, макс. здоровье
        """
        if ship:
            space_ship_field = 25 - len(ship.name)
            ship_hp = f'{ship.health}\\{ship.MAX_HEALTH}'
            return ship.name + '_' * space_ship_field + ship_hp
        elif not ship:
            return Fore.LIGHTBLACK_EX + '*' * 10 + '_' * 6 + '\\' * 8 + Style.RESET_ALL  # Death string

    def screen(self):
        """
        Функция отрисовывает построчно поле игры, собирая в итерации цикла строку из аттрибутов объектов кораблей
        :return: Визуальное отображение игры в консоли
        """
        self.clear_screen()
        # Отрисовка
        print('\n')
        print(self.teams[0].name + self.space(self.teams[0].name) + self.teams[1].name)

        for i in range(Team.SIZE):
            ship_1, ship_2 = self.teams[0].ships[i], self.teams[1].ships[i]
            string_1, string_2 = self.ship_field(ship_1), self.ship_field(ship_2)

            print(string_1 + self.space(string_1) + string_2)

    async def screen_loop(self):
        while self.running:
            self.screen()
            await asyncio.sleep(3)

    async def actions_loop(self, ship, team_enemy):
        while self.running and ship in ship.team.ships:
            if hasattr(ship, 'weapon'):
                targets = [i for i in team_enemy.ships if i is not None]
                if targets:
                    enemy = choice(targets)
                    ship.take_enemy(enemy)
                else:
                    self.endgame(ship.team)
            if hasattr(ship, 'storage'):
                pass
            if hasattr(ship, 'shield'):
                pass
            if hasattr(ship, 'repair_team'):
                pass
            await asyncio.sleep(ship.attack_speed) if hasattr(ship, 'attack_speed') else await asyncio.sleep(10)

    def endgame(self, winner):
        self.running = False
        self.screen()
        print('\n')
        print(f'{winner.name} is winner')

    async def main(self):
        screen = asyncio.create_task(self.screen_loop())
        loops = [screen]
        for team in self.teams:
            enemy_team = self.teams[1] if team == self.teams[0] else self.teams[0]
            for ship in team.ships:
                actions = asyncio.create_task(self.actions_loop(ship, enemy_team))
                loops.append(actions)
        await asyncio.gather(*loops)


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    asyncio.run(btf.main())
