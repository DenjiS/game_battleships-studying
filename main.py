from objects.ships import *
from time import sleep
from colorama import Fore, Style
import os
from concurrent.futures import ThreadPoolExecutor
from threading import RLock

# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    SIZE = 5

    def __init__(self, name, color):
        self.color = color
        self.name = color + name + Style.RESET_ALL
        self.size = self.SIZE

        self.ships = []
        for num in range(self.SIZE):
            # Создание объекта корабля
            append_ship = choice(ship_types_list)(self, num)
            self.ships.append(append_ship)


class Battlefield:
    def __init__(self, *teams):
        # Инициализация команд
        self.teams = teams
        self.running = True

    def mainloop(self):
        with ThreadPoolExecutor(max_workers=11) as ex:
            ex.submit(self.screen_thread)
            for i in range(10):
                team = i % 2
                num = int(i / 2)
                ship = self.teams[team].ships[num]
                team_enemy = self.teams[1] if team == 0 else self.teams[0]
                ex.submit(self.actions_thread, ship, team_enemy)

    def actions_thread(self, ship, team_enemy):
        while ship.health > 0:
            if team_enemy.size > 0:
                ship.actions(team_enemy)
            else:
                self.endgame()
                break

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
            ship_hp = f'{ship.health}\\{ship.MAX_HEALTH}\\{ship.armor}'
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

    def screen_thread(self):
        scr_lock = RLock()
        while self.running:
            scr_lock.acquire()
            self.screen()
            scr_lock.release()
            sleep(2.5)

    def endgame(self):
        self.clear_screen()
        winner = self.teams[0] if any(self.teams[0].ships) else self.teams[1]
        print(f'\n{winner.name} is winner')
        self.screen()
        self.running = False


if __name__ == '__main__':
    team_red, team_blue = Team('RED', Fore.RED), Team('BLUE', Fore.BLUE)
    btf = Battlefield(team_red, team_blue)
    btf.mainloop()
