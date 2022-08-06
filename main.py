from ships import *
from random import randint
from time import sleep
from colorama import Fore, Style
import os

# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    def __init__(self, name, color):
        self.color = color
        self.name = color + name + Style.RESET_ALL
        self.ships = []
        # Добавление кораблей в команду
        for count in range(5):
            rand_int = randint(0, 4)
            # Создание объекта корабля
            append_ship = ship_types_list[rand_int](self, count)
            self.ships.append(append_ship)


class Battlefield:
    def __init__(self):
        # Инициализация команд
        self.team_1 = Team('RED', Fore.RED)
        self.team_2 = Team('BLUE', Fore.BLUE)

    def mainloop(self):
        while True:
            clear = lambda: os.system('cls')
            clear()
            self.screen(self.team_1, self.team_2)
            sleep(0.1)
            for i in range(5):
                # Корабль первой команды
                ship = self.team_1.ships[i]
                enemy = self.team_2.ships[randint(0, 4)]
                if hasattr(ship, 'weapon'):
                    ship.shoot(target=enemy)
                    sleep(0.5)
                # Корабль второй команды
                ship = self.team_2.ships[i]
                enemy = self.team_1.ships[randint(0, 4)]
                if hasattr(ship, 'weapon'):
                    ship.shoot(target=enemy)
                    sleep(0.5)

    @staticmethod
    def screen(team_1, team_2):
        """
        Функция отрисовывает построчно поле игры, собирая в итерации цикла строку из аттрибутов объектов кораблей
        :return: Визуальное отображение игры в консоли
        """

        def ship_field(ship):
            if not ship.dead:
                ship_name = f'{ship.name}'
                space = 25 - len(ship_name)
                ship_hp = f'{ship.health}\\{ship.MAX_HEALTH}'
                return ship_name + '_' * space + ship_hp + Style.RESET_ALL
            elif ship.dead or not ship:
                ship = None
                return death_string

        space_team = 65 - len(team_1.name)
        death_string = '*' * 10 + '_' * 6 + '\\' * 8 + Style.RESET_ALL

        print('\n')
        print(team_1.name + ' ' * space_team + team_2.name)
        for i in range(5):
            ship_1, ship_2 = team_1.ships[i], team_2.ships[i]
            string_1, string_2 = ship_field(ship_1), ship_field(ship_2)
            # Colorama problem
            if not ship_1.dead:
                space = 65 - len(string_1)
            elif ship_1.dead:
                space = 56 - len(string_1)

            print(string_1 + ' ' * space + string_2)


if __name__ == '__main__':
    btf = Battlefield()
    btf.mainloop()
