from ships import *
from random import randint
from time import sleep
import os

# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    def __init__(self, name):
        self.name = name
        self.ships = []
        # Добавление кораблей в команду
        for count in range(5):
            rand_int = randint(0, 4)
            # Создание объекта корабля
            append_ship = ship_types_list[rand_int]()
            self.ships.append(append_ship)


class Battlefield:
    def __init__(self):
        # Инициализация команд
        self.team_1 = Team('A')
        self.team_2 = Team('B')

    @staticmethod
    def shoot(i, team_shooter, team_victim):
        if hasattr(team_shooter.ships[i], 'weapon'):
            rand_int = randint(0, 4)
            team_victim.ships[rand_int].health -= team_shooter.ships[i].weapon.dmg

    def mainloop(self):
        while True:
            clear = lambda: os.system('cls')
            clear()
            self.screen(self.team_1, self.team_2)
            sleep(1)
            for i in range(5):
                try:
                    self.shoot(i, self.team_1, self.team_2)
                    if self.team_2.ships[i].dead:
                        self.team_2.ships[i] = None
                except AttributeError:
                    pass
                try:
                    self.shoot(i, self.team_2, self.team_1)
                    if self.team_1.ships[i].dead:
                        self.team_1.ships[i] = None
                except AttributeError:
                    pass

    @staticmethod
    def screen(team_1, team_2):
        """
        Функция отрисовывает построчно поле игры, собирая в итерации цикла строку из аттрибутов объектов кораблей
        :return: Визуальное отображение игры в консоли
        """
        for i in range(5):
            # Данные корабля первой команды
            try:
                team_1_ship_name = f'{team_1.ships[i].name}'
                space_1 = 15 - len(team_1_ship_name)
                team_1_ship_hp = f'{team_1.ships[i].health}\\{team_1.ships[i].MAX_HEALTH}'
            except AttributeError:
                team_1_ship_name = '********'
                space_1 = 2
                team_1_ship_hp = '********'
            # Пространство между полями команд
            space_between = 40 - len(team_1_ship_hp)
            # Данные корабля второй команды
            try:
                team_2_ship_name = f'{team_2.ships[i].name}'
                space_2 = 15 - len(team_2_ship_name)
                team_2_ship_hp = f'{team_2.ships[i].health}\\{team_2.ships[i].MAX_HEALTH}'
            except AttributeError:
                team_2_ship_name = '********'
                space_2 = 2
                team_2_ship_hp = '********'
            # Вывод строки
            print(team_1_ship_name + '_' * space_1 + team_1_ship_hp +
                  ' ' * space_between +
                  team_2_ship_name + '_' * space_2 + team_2_ship_hp)


if __name__ == '__main__':
    btf = Battlefield()
    btf.mainloop()
