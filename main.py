from objects.ships import *
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


class Battlefield:
    def __init__(self, *teams):
        # Инициализация команд
        self.teams = teams
        self.running = True

    def battle_gen(self, teams):
        iters = [iter(i.ships) for i in teams]
        turn = 0
        while teams:
            yield next(iters[turn])
            if turn == 0:
                turn = 1
            else:
                turn = 0

    def mainloop(self):
        gen = self.battle_gen(self.teams)
        while self.running:
            self.clear_screen()
            self.screen()
            sleep(0.5)

            ship = next(gen)
            enemy_team = self.teams[1] if ship.team == self.teams[0] else self.teams[0]
            if ship:
                ship.actions(enemy_team)

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

    def endgame(self, winner):
        self.clear_screen()
        print('\n')
        print(f'{winner.name} is winner')
        self.screen()
        self.running = False


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.mainloop()
