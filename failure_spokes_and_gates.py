from itertools import combinations_with_replacement, combinations
import random

NUMBER_OF_TEAMS = 6

sectors_capacity = {
    "Сектор 1": 2,
    "Сектор 2'": 4,
    # "Сектор 'Металл'": 4,
    "Сектор 3": 2
}

sum_of_capacity = sum(sectors_capacity.values())

if NUMBER_OF_TEAMS > sum_of_capacity:
    print("Количество команд больше суммарного объема секторов!")
    print(f"Количество команд: {NUMBER_OF_TEAMS}")
    print(f"Сумма объемов секторов: {sum_of_capacity}")
    exit()

# Количество секторов
sectors_num = len(sectors_capacity)

# Отсортируем словарь sectors_capacity
sectors_capacity = {k: v for k, v in sorted(sectors_capacity.items(), key=lambda x: x[1], reverse=False)}

# # Список сочетаний по две команды
# teams = list(range(1, NUMBER_OF_TEAMS + 1))
# combinations_list = list(combinations_with_replacement(teams, 2))
# combinations_list = [combo for combo in combinations_list if combo[0] != combo[1]]

# Список комбинаций по две команды
teams = list(range(1, NUMBER_OF_TEAMS + 1))
combinations_list = list(combinations(teams, 2))
combinations_list += [combo[::-1] for combo in combinations_list]

sectors_history = {key: [] for key in sectors_capacity.keys()}
no_freeze = 0
for _ in range(sectors_num):
    assigned_teams = []
    teams_list = list(range(1, NUMBER_OF_TEAMS + 1))
    for current_sector, current_capacity in sectors_capacity.items():
        print(f'{current_sector}: ', end='')
        for i in range(int(current_capacity/2)):
            while True:
                team_pair = random.choice(combinations_list)
                team_1, team_2 = team_pair
                if team_1 not in assigned_teams and team_2 not in assigned_teams:
                    if team_1 not in sectors_history[current_sector] and team_2 not in sectors_history[current_sector]:
                        break
                no_freeze += 1
                if no_freeze > 500:
                    print()
                    print('='*40)
                    print('Программа зависла. Решение не найдено.')
                    print('='*40)
                    exit()
            combinations_list.pop(combinations_list.index(team_pair))
            for team in team_pair:
                assigned_teams.append(team)
                temp_list = [*sectors_history[current_sector], team]
                sectors_history[current_sector] = temp_list
                teams_list.pop(teams_list.index(team))
            print(f'{team_pair}', end=', ')
            if len(teams_list) == 0:
                break
        print()
    print('----- Смена секторов -----')
