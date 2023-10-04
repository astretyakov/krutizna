import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime
import tasks_count


def db_frame_creation():
    # Открываем диалоговое окно выбора файла
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Проверяем, был ли выбран файл
    if file_path:
        return pd.read_csv(file_path)
    else:
        return None


def tasks_processing(db_base, db_loading_list, db_tasks_layout, task_name, task_quantity):
    # Проверяем наличие значения task_name в базе данных
    if task_name not in db_base.columns:
        print(f"'{task_name}' отсутствует в базе данных")
        return

    # Находим столбцы db_base по значению task_name
    columns = [col for col in db_base.columns if col.find(task_name) != -1]

    # Ищем строки, в которых есть значения в найденных столбцах
    rows = db_base.loc[db_base[columns].notna().any(axis=1)]

    # Добавляем значения найденных строк в db_loading_list
    for index, row in rows.iterrows():
        if row[task_name] > 0:
            db_loading_list.loc[len(db_loading_list)] = [row['Наименование'], row[task_name] * task_quantity, False,
                                                         task_name]
            db_tasks_layout.loc[len(db_tasks_layout)] = [row['Наименование'], row[task_name], task_name]
    return


def summed_loading_list(dataframe):
    return dataframe.groupby("Наименование").agg({"Кол-во": "sum", "Checkbox": "first", "Для задания": "first"}).reset_index()


def main(tasks_count_loc):
    if not tasks_count_loc:
        print('Список заданий не определён.')
        return

    database = db_frame_creation()

    # Создаём новый датафрейм, в который будем записывать список погрузки
    loading_list = pd.DataFrame(columns=["Наименование", "Кол-во", "Checkbox", "Для задания"])

    # Создаём новый датафрейм с раскладкой заданий
    tasks_layout = pd.DataFrame(columns=["Наименование", "Кол-во", "Для задания"])

    for task_name, quantity in tasks_count.items():
        tasks_processing(database, loading_list, tasks_layout, task_name, quantity)

    # print(loading_list)  # Вывод по заданиям без суммирования одинаковых позиций

    # Текущая дата
    current_date = datetime.datetime.now().strftime('%Y%m%d')

    # Сохраняем список погрузки
    filename = f'loading_list_{current_date}.csv'
    loading_list.to_csv(filename, index=False)

    # Сохраняем раскладку заданий
    tasks_layout_filename = f'tasks_layout_{current_date}.csv'
    tasks_layout.to_csv(tasks_layout_filename, index=False)

    # === Создание файла с проссумированными позициями === #
    # # Создать имя файла с текущей датой
    # filename = f'summed_loading_list_{current_date}.csv'
    #
    # # Сохранить данные в файл
    # summed_loading_list(loading_list).to_csv(filename, index=False)
    # ================================================ #


if __name__ == "__main__":
    tasks_count = tasks_count.tasks_count
    main(tasks_count)
    # print(len(tasks_count))
    # k = 0
    # for key, value in tasks_count.items():
    #     k += value
    # print(k)
