
from datetime import datetime, timedelta

#в форме пока такие есть длины лекций:
duration_mapping = {
    '30 минут': timedelta(minutes=30),
    '1 час': timedelta(hours=1),
    '1,5 часа': timedelta(hours=1, minutes=30),
    '7 дней': timedelta(days=7),
    '3 дня': timedelta(days=7),
    '5 минут': timedelta(minutes=5),
}

# конверторы
def convert_duration(duration_from_form: str) -> timedelta:
    return duration_mapping.get(duration_from_form)
def convert_date(date_from_form: str) -> datetime:
    return datetime.strptime(date_from_form, '%d.%m.%Y %H:%M:%S')

# считатели
def sum_date_and_duration(date: datetime, duration: timedelta) -> datetime:
    return date+duration
def subtract_date_and_duration(date: datetime, duration: timedelta) -> datetime:
    return date-duration

# пример использования
date_from_dict_of_form = '24.05.2024 20:21:59'
duration_from_dict_of_form = '7 дней'
converted_duration = convert_duration(duration_from_dict_of_form)
converted_date = convert_date(date_from_dict_of_form)
print(f"{date_from_dict_of_form} --> {converted_date}")
print(f"{duration_from_dict_of_form} --> {converted_duration}")
print(f"Their subtraction = {subtract_date_and_duration(converted_date, converted_duration)}")
print(f"Their sum = {sum_date_and_duration(converted_date, converted_duration)}")
""" 
    ВЫВОД:
24.05.2024 20:21:59 --> 2024-05-24 20:21:59
7 дней --> 7 days, 0:00:00
Their subtraction = 2024-05-17 20:21:59
Their sum = 2024-05-31 20:21:59
"""