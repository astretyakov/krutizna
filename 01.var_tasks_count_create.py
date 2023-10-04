import tkinter as tk
from tkinter import filedialog

# Создаем окно с выбором файла
root = tk.Tk()
root.withdraw()

# Запрашиваем путь к файлу .csv
file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

# Читаем файл и составляем словарь
tasks_count = {}
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines[1:]:  # Пропускаем первую строку с заголовками
        name, count = line.strip().split(',')
        if count.isdigit():  # Проверяем, является ли значение числом
            tasks_count[name] = int(count)

# Формируем строку вывода
output = "tasks_count = {\n"
for name, count in tasks_count.items():
    output += f"    '{name}': {count},\n"
output += "}"

# Сохраняем вывод в файл tasks_count.py
with open('tasks_count.py', 'w', encoding='utf-8') as output_file:
    output_file.write(output)

# Выводим информацию о сохранении
print("Файл tasks_count.py успешно сохранен.")
