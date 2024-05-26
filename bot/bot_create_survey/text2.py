import datetime
from converters import convert_date

def convert_date(date_from_form: str) -> datetime:
    return datetime.datetime.strptime(date_from_form, "%d.%m.%Y %H:%M:%S")

def get_lecture():
    return [{'name': "lection1", 'date': '28.06.2024 11:00:00'},
            {'name': "lection2", 'date': '28.07.2024 11:00:00'},
            {'name': "lection3", 'date': '28.06.2024 11:00:00'},
            {'name': "lection4", 'date': '28.05.2024 11:00:00'}]

def compare_to_month(month: int):
    for lecture in get_lecture():
        month_of_lecture = convert_date(lecture["date"]).month
        if month_of_lecture == month:
            print(lecture['name'])

compare_to_month(6)