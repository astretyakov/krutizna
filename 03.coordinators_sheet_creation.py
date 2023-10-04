import pandas as pd
from tabulate import tabulate


def make_tasks_dataframe():
    tasks_list = [['Обед']]
    for key, value in tasks_count.items():
        for i in range(1, value + 1):
            # tasks_list.append([key])
            # С номером после задания
            tasks_list.append([f'{key} {i}'])
    tasks_list.append(['Финал'])
    df = pd.DataFrame(tasks_list, columns=['Задания'])
    # Добавляем пустые колонки
    for i in range(teams_count):
        df[i + 1] = ''
    return df


def number_of_teams_count(people_num, teams_count_loc=None):
    if teams_count_loc:
        return teams_count_loc

    if people_num <= 15:
        return 1
    elif 16 <= people_num <= 60:
        return (people_num // 11) + (people_num % 11 > 0)
    elif 61 <= people_num <= 100:
        return (people_num // 12) + (people_num % 12 > 0)
    else:
        return (people_num // 13) + (people_num % 13 > 10)


if __name__ == '__main__':
    # ================ Данные по мероприятию ================
    event_date = '2023-10-05'
    number_of_people = 100
    file_name = f'{event_date}. ЛК. {number_of_people} чел'
    # =======================================================
    tasks_count = {
        'Нога в ногу': 2,
        'Лыжи': 2,
        'Змейка': 1,
        'Гусеница': 2,
        'Лабиринт': 2,
        'Паутинка': 2,
        'Встреча': 2,
        'Лабиринт 2Ш': 1,
        '3D-куб': 2,
        'Двойной мост': 1,
        'Фигура': 1,
        'Мост Леонардо': 1,
        'Морской узел': 1,
        'Обруч': 1,
        'Шашлык': 2,
        'Колобок': 1,
        'По росту': 1,
        'Шаман': 1,
    }

    # teams_count = number_of_teams_count(number_of_people)
    teams_count = number_of_teams_count(number_of_people, 10)

    tasks_dataframe = make_tasks_dataframe()
    tasks_dataframe['Задания'] = tasks_dataframe['Задания'].apply(lambda x: x.zfill(3))

    # print(tabulate(tasks_dataframe, headers='keys', tablefmt='grid'))

    # Save dataframe as txt with borders
    with open(f'{file_name}.txt', 'w') as f:
        f.write(tabulate(tasks_dataframe, headers='keys', tablefmt='grid'))

    # Save dataframe as csv file
    tasks_dataframe.to_csv(f'{file_name}.csv', index=False)

    # Статистика
    statistics = [
        ['Дата мероприятия:', event_date],
        ['Количество людей:', number_of_people],
        ['Количество команд:', teams_count],
        ['Всего заданий:', tasks_dataframe.shape[0] - 2],
        ['Лист координатора сохранён\nв двух файлах с именами:', f'"{file_name}.txt/csv"']
    ]
    print(tabulate(statistics, tablefmt='grid'))
