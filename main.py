from objects.ships import *
from random import choice
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
        for num in range(5):
            # Создание объекта корабля
            append_ship = choice(ship_types_list)(self, num)
            self.ships.append(append_ship)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def space(obj):
    return ' ' * (65 - len(obj))


def ship_field(ship):
    if ship:
        space_ship_field = 25 - len(ship.name)
        ship_hp = f'{ship.health}\\{ship.MAX_HEALTH}'
        return ship.name + '_' * space_ship_field + ship_hp
    elif not ship:
        return Fore.LIGHTBLACK_EX + '*' * 10 + '_' * 6 + '\\' * 8 + Style.RESET_ALL  # Death string


class Battlefield:
    def __init__(self, team_1, team_2):
        # Инициализация команд
        self.team_1, self.team_2 = team_1, team_2
        self.running = True

    def mainloop(self):
        while True:
            # Очистка CLI
            clear_screen()

            self.screen()
            sleep(0.1)

            for i in range(5):
                self.actions(i, self.team_1, self.team_2)
                self.actions(i, self.team_2, self.team_1)

            if not self.running:
                break

    def screen(self):
        """
        Функция отрисовывает построчно поле игры, собирая в итерации цикла строку из аттрибутов объектов кораблей
        :return: Визуальное отображение игры в консоли
        """

        # Отрисовка
        print('\n')
        print(self.team_1.name + space(self.team_1.name) + self.team_2.name)

        for i in range(5):
            ship_1, ship_2 = self.team_1.ships[i], self.team_2.ships[i]
            string_1, string_2 = ship_field(ship_1), ship_field(ship_2)

            print(string_1 + space(string_1) + string_2)

    def actions(self, num, team_ally, team_enemy):
        ship = team_ally.ships[num]

        if hasattr(ship, 'weapon'):
            if any(team_enemy.ships):
                enemy = choice(team_enemy.ships)
                if enemy:
                    ship.take_enemy(enemy)
                    sleep(0.5)
                else:
                    self.actions(num, team_ally, team_enemy)
            else:
                self.endgame(team_ally)

    def endgame(self, winner):
        clear_screen()
        print('\n')
        print(f'{winner.name} is winner')
        self.screen()
        self.running = False


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.mainloop()
