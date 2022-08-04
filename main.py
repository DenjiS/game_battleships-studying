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
        print('\n')
        space = 65 - len(team_1.name)
        death_string = '*' * 10 + '_' * 6 + '\\' * 8
        print(team_1.name + ' ' * space + team_2.name)
        for i in range(5):
            # Данные корабля первой команды
            ship_1 = team_1.ships[i]
            if not ship_1.dead:
                ship_1_name = f'{ship_1.name}'
                space_1 = 25 - len(ship_1_name)
                ship_1_hp = f'{ship_1.health}\\{ship_1.MAX_HEALTH}'
                string_1 = ship_1_name + '_' * space_1 + ship_1_hp
            elif ship_1.dead or not ship_1:
                ship_1 = None
                string_1 = death_string
            # Пространство между полями команд
            if string_1 != death_string:
                space_between = 65 - len(string_1)
            elif string_1 == death_string:
                space_between = 56 - len(string_1)
            # Данные корабля второй команды
            ship_2 = team_2.ships[i]
            if not ship_2.dead:
                ship_2_name = f'{ship_2.name}'
                space_2 = 25 - len(ship_2_name)
                ship_2_hp = f'{ship_2.health}\\{ship_2.MAX_HEALTH}'
                string_2 = ship_2_name + ('_' * space_2) + ship_2_hp
            elif ship_2.dead or not ship_2:
                ship_2 = None
                string_2 = death_string

            print(string_1 + Style.RESET_ALL + ' ' * space_between + string_2)


if __name__ == '__main__':
    btf = Battlefield()
    btf.mainloop()
