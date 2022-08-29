from objects.ships import *
from random import choice
from time import sleep
from colorama import Fore, Style
import os

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


class BattleIter:
    def __init__(self, teams):
        self.teams = teams
        self.count = 0
        self.turn = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= Team.SIZE:
            self.count = 0
        if self.turn and any(self.teams[1].ships):
            self.turn = False
            return self.teams[0].ships[self.count], self.teams[1]
        elif not self.turn and any(self.teams[0].ships):
            self.turn = True
            self.count += 1
            return self.teams[1].ships[self.count - 1], self.teams[0]
        else:
            raise StopIteration


class Battlefield:
    def __init__(self, *teams):
        # Инициализация команд
        self.teams = teams
        self.running = True

    def __iter__(self):
        return BattleIter(self.teams)

    def mainloop(self):
        btf_iter = iter(self)
        while self.running:
            self.screen()
            sleep(0.1)
            try:
                args = next(btf_iter)
                self.actions(*args)
            except StopIteration:
                self.endgame()

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

    @classmethod
    def actions(cls, ship, team_enemy):
        if hasattr(ship, 'weapon'):
            targets = [i for i in team_enemy.ships if i is not None]
            enemy = choice(targets)
            ship.take_enemy(enemy)

    def endgame(self):
        self.screen()
        print('\n')
        print('FINISH')
        self.running = False


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.mainloop()
