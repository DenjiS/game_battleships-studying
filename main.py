from ships import *
from random import randint


# Типы кораблей
ship_types_list = [Jet, HeavyJet, Cruiser, CargoShip, RepairShip]


class Team:
    def __init__(self):
        self.ship_list = []
        # Добавление кораблей в команду
        for count in range(5):
            rand_int = randint(0, 4)
            # Создание объекта корабля
            append_ship = ship_types_list[rand_int]()
            self.ship_list.append(append_ship)

    def ship(self, num):
        return self.ship_list[num]


# Инициализация команд
team_1 = Team()
team_2 = Team()
print(team_1, team_2)
# Вывод игровых объектов в консоль
for i in range(5):
    # Данные корабля первой команды
    team_1_ship_name = f'{team_1.ship(i).name}'
    space_1 = 15 - len(team_1_ship_name)
    team_1_ship_hp = f'{team_1.ship(i).health}\\{team_1.ship(i).MAX_HEALTH}'
    # Пространство между полями команд
    space_between = 40 - len(team_1_ship_hp)
    # Данные корабля второй команды
    team_2_ship_name = f'{team_2.ship(i).name}'
    space_2 = 15 - len(team_2_ship_name)
    team_2_ship_hp = f'{team_2.ship(i).health}\\{team_2.ship(i).MAX_HEALTH}'
    # Вывод строки
    print(team_1_ship_name + '_' * space_1 + team_1_ship_hp +
          ' ' * space_between +
          team_2_ship_name + '_' * space_2 + team_2_ship_hp)
