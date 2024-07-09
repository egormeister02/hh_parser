import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import filedialog
from tkinter import simpledialog
import threading
import requests
import time
import pandas as pd
import os

import periods as pr

URL = 'https://api.hh.ru/vacancies'

schedule_descriptions = {
    'fullDay': 'Полный день',
    'shift': 'Сменный график',
    'flexible': 'Гибкий график',
    'remote': 'Удаленная работа',
    'flyInFlyOut': 'Вахтовый метод'
}
def split_interval(date_from, date_to):
    """Функция для разбиения интервала на два равных интервала."""
    half_duration = (date_to - date_from) / 2
    middle_date = date_from + half_duration
    return (date_from, middle_date), (middle_date, date_to)

def getVacans(url, params):
    vacancies = []
    page = 0
    while True:
        time.sleep(0.05)  # Задержка между запросами
        params['page'] = page
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f'Ошибка при выполнении запроса к API hh.ru: {response.status_code}, График работы: ' + str(params['schedule']))

            break

        data = response.json()

        for item in data['items']:
            employer = item.get('employer', {})
            vacancies.append({
                'Наименование вакансии': item.get('name'),
                'Ссылка': item.get('alternate_url'),
                'Имя компании': employer.get('name', 'Не указано'),
                'Ссылка на компанию': employer.get('alternate_url', 'Не указано'), 
                'График работы': schedule_descriptions.get(params.get('schedule'),'Не указано')
            })

        if (page + 1) >= data['pages']:
            break
        page += 1
    time.sleep(1.5)
    return vacancies

def fetch_vacancies(job_title):
    
    times_fullday = pr.getFulldayPeriods()
    times_remote = pr.getRemorePeriods(times_fullday)
    times_else = pr.getElsePeriods()

    all_vacancies = []

    for schedule in schedule_descriptions.keys():
        if schedule == 'fullDay':
            for date_from_str, date_to_str in times_fullday:  # Исправлено на корректную распаковку кортежей
                params = {
                    'text': job_title,
                    'area': '113',
                    'per_page': '100',
                    'search_field': 'name',
                    'schedule': schedule,
                    'date_from': date_from_str,
                    'date_to': date_to_str,
                }

                vacancies = getVacans(URL, params)
                all_vacancies.extend(vacancies)  # Исправлено на добавление непосредственно в all_vacancies

        if schedule == 'remote':
            for date_from_str, date_to_str in times_remote:  # Исправлено на корректную распаковку кортежей
                params = {
                    'text': job_title,
                    'area': '113',
                    'per_page': '100',
                    'search_field': 'name',
                    'schedule': schedule,
                    'date_from': date_from_str,
                    'date_to': date_to_str,
                }

                vacancies = getVacans(URL, params)
                all_vacancies.extend(vacancies)  # Исправлено на добавление непосредственно в all_vacancies

        else:
            for date_from_str, date_to_str in times_else:  # Исправлено на корректную распаковку кортежей
                params = {
                    'text': job_title,
                    'area': '113',
                    'per_page': '100',
                    'search_field': 'name',
                    'schedule': schedule,
                    'date_from': date_from_str,
                    'date_to': date_to_str,
                }

                vacancies = getVacans(URL, params)
                all_vacancies.extend(vacancies)  # Исправлено на добавление непосредственно в all_vacancies

    return all_vacancies

def center_window(window, width, height):
    # Получаем размеры экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Вычисляем x и y координаты для размещения окна в центре экрана
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def on_closing():
    os._exit(0)

def save_to_excel(vacancies, filename):
    if vacancies:
        df = pd.DataFrame(vacancies)
        df.to_excel(filename, index=False, engine='openpyxl')
        # Вместо print используем messagebox для оповещения пользователя
        tk.messagebox.showinfo("Сохранение завершено", f'Данные о вакансиях успешно сохранены в файл {filename}')
    else:
        tk.messagebox.showinfo("Ошибка", 'Вакансии не найдены или произошла ошибка.')

def search_vacancies():
    job_title = simpledialog.askstring("Поиск вакансий", "Введите наименование вакансии:")
    if not job_title:
        return
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not filename:
        return
    
    # Создаем и отображаем окно загрузки
    loading_window = tk.Toplevel(root)
    center_window(loading_window, 300, 100)  # поместите вашу функцию center_window здесь, если она у вас в другом месте
    loading_window.title("Загрузка")
    tk.Label(loading_window, text="Идет загрузка данных,\n пожалуйста, подождите...").pack(padx=20, pady=20)
    loading_window.update()  # обновляем окно, чтобы оно отобразилось до начала загрузки
    
    def async_fetch_save():
        vacancies = fetch_vacancies(job_title)
        save_to_excel(vacancies, filename)
        loading_window.destroy()  # закрываем окно загрузки после завершения сохранения
    
    threading.Thread(target=async_fetch_save).start()

root = tk.Tk()
root.title("Поиск вакансий на hh.ru")
center_window(root, 480, 320)
root.protocol("WM_DELETE_WINDOW", on_closing)
search_button = tk.Button(root, text="Искать вакансии", command=search_vacancies)
search_button.pack(pady=20)


root.mainloop()
