import time
from datetime import datetime, timedelta
import pytz

TIME_ZONE = pytz.timezone('Europe/Moscow')

def split_interval(date_from, date_to):
    half_duration = (date_to - date_from) / 2
    middle_date = date_from + half_duration
    return (date_from, middle_date), (middle_date, date_to)

def getFulldayPeriods():
    
    times_fullday = []
    day_shift = 1

    for day in range(3):
        date_to = datetime.now(TIME_ZONE) - timedelta(days=day)
        date_from = date_to - timedelta(days=day_shift)
        first_half, second_half = split_interval(date_from, date_to)
        times_fullday.extend([first_half, second_half])

    # Форматирование временных интервалов в строковом представлении сразу после создания
    formatted_times_fullday = []
    for interval in times_fullday:
        date_from_str = interval[0].strftime("%Y-%m-%dT%H:%M:%S%z")
        date_to_str = interval[1].strftime("%Y-%m-%dT%H:%M:%S%z")
        formatted_times_fullday.append((date_from_str, date_to_str))

    # Итоговый массив временных интервалов
    times_fullday = formatted_times_fullday

        # Предыдущая точка отсчета (например, дата за 3 дня до `datetime.now()`)
    previous_date_to = datetime.now(TIME_ZONE) - timedelta(days=3)

    # Добавляем новые промежутки
    # Два промежутка по одному дню каждый
    for i in range(2):
        date_to = previous_date_to
        date_from = date_to - timedelta(days=1)
        times_fullday.append((date_from.strftime("%Y-%m-%dT%H:%M:%S%z"), date_to.strftime("%Y-%m-%dT%H:%M:%S%z")))
        previous_date_to = date_from

    # Два промежутка по два дня каждый
    for i in range(2):
        date_to = previous_date_to
        date_from = date_to - timedelta(days=2)
        times_fullday.append((date_from.strftime("%Y-%m-%dT%H:%M:%S%z"), date_to.strftime("%Y-%m-%dT%H:%M:%S%z")))
        previous_date_to = date_from

    # Один промежуток равный неделе
    date_to = previous_date_to
    date_from = date_to - timedelta(weeks=1)
    times_fullday.append((date_from.strftime("%Y-%m-%dT%H:%M:%S%z"), date_to.strftime("%Y-%m-%dT%H:%M:%S%z")))
    previous_date_to = date_from

    # Один промежуток равный месяцу
    date_to = previous_date_to
    date_from = date_to - timedelta(days=30)  # Аппроксимация месяца
    times_fullday.append((date_from.strftime("%Y-%m-%dT%H:%M:%S%z"), date_to.strftime("%Y-%m-%dT%H:%M:%S%z")))

    # Итоговый массив временных интервалов обновлен

    times_fullday = sorted(times_fullday, key=lambda x: x[0])

    return times_fullday

def getRemorePeriods(fulldayPeriods):
    times_remote = []

    for i in range(0, len(fulldayPeriods) - 1, 2):
        # Объединяем каждую пару интервалов
        start = fulldayPeriods[i][0]  # Начало текущего интервала
        end = fulldayPeriods[i + 1][1]  # Конец следующего интервала в паре
        times_remote.append((start, end))
    
    return times_remote

def getElsePeriods():
    
    end_of_last_interval = datetime.now(TIME_ZONE)
    # Создаем недельный интервал
    week_interval_end = end_of_last_interval
    week_interval_start = week_interval_end - timedelta(weeks=1)

    # Создаем месячный интервал следующим за недельным
    month_interval_end = week_interval_start
    month_interval_start = month_interval_end - timedelta(days=30)  # Примерное представление месяца

    # Формируем новые интервалы в правильном формате строки
    week_interval = (week_interval_start.strftime("%Y-%m-%dT%H:%M:%S%z"), week_interval_end.strftime("%Y-%m-%dT%H:%M:%S%z"))
    month_interval = (month_interval_start.strftime("%Y-%m-%dT%H:%M:%S%z"), month_interval_end.strftime("%Y-%m-%dT%H:%M:%S%z"))

    # Создаем массив times_3
    return [month_interval, week_interval]
