from objects.ships import *
from random import choice
from colorama import Fore, Style
import os
import asyncio

# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    def __init__(self, name, color):
        self.color = color
        self.name = color + name + Style.RESET_ALL

        self.ships = []
        for num in range(5):
            # Создание объекта корабля
            append_ship = choice(ship_types_list)(self, num)
            self.ships.append(append_ship)

            self.count = -1

    def __iter__(self):
        return self

    def __next__(self):
        if not any(self.ships):
            raise StopIteration
        self.count += 1
        if self.count >= len(self.ships):
            self.count = 0
        return self.ships[self.count]


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

        # Отрисовка
        print('\n')
        print(self.teams[0].name + self.space(self.teams[0].name) + self.teams[1].name)

        for i in range(5):
            ship_1, ship_2 = self.teams[0].ships[i], self.teams[1].ships[i]
            string_1, string_2 = self.ship_field(ship_1), self.ship_field(ship_2)

            print(string_1 + self.space(string_1) + string_2)

    async def screen_loop(self):
        while self.running:
            self.clear_screen()
            self.screen()
            await asyncio.sleep(5)

    @classmethod
    async def actions(cls, ship, team_enemy):
        if hasattr(ship, 'weapon') and ship.reloaded and team_enemy:
            targets = [i for i in team_enemy.ships if i is not None]
            enemy = choice(targets)
            ship.take_enemy(enemy)
            ship.reloaded = False
            await asyncio.sleep(ship.attack_speed)
        if hasattr(ship, 'storage'):
            pass
        if hasattr(ship, 'shield'):
            pass
        if hasattr(ship, 'repair_team'):
            pass
        try:
            ship.reloaded = True
        except AttributeError:
            pass
        finally:
            await asyncio.sleep(0)

    def endgame(self, winner):
        self.running = False
        self.clear_screen()
        print('\n')
        print(f'{winner.name} is winner')
        self.screen()

    async def battle_loop(self, team):
        enemy_team = self.teams[1] if team == self.teams[0] else self.teams[0]
        while self.running:
            if not any(team):
                self.endgame(enemy_team)
                break
            for i in team:
                await self.actions(i, enemy_team)

    async def main(self):
        loop_1 = asyncio.create_task(self.battle_loop(self.teams[0]))
        loop_2 = asyncio.create_task(self.battle_loop(self.teams[1]))
        screen = asyncio.create_task(self.screen_loop())
        await screen
        await loop_1
        await loop_2


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    asyncio.run(btf.main())
