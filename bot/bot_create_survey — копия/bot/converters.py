import datetime


def convert_date(date_from_form: str) -> datetime:
    return datetime.datetime.strptime(date_from_form, "%d.%m.%Y %H:%M:%S")


duration_mapping = {
    "30 минут": datetime.timedelta(minutes=30),
    "1 час": datetime.timedelta(hours=1),
    "1,5 часа": datetime.timedelta(hours=1, minutes=30),
    "7 дней": datetime.timedelta(days=7),
    "3 дня": datetime.timedelta(days=7),
    "5 минут": datetime.timedelta(minutes=5),
}


def convert_duration(duration_from_form: str) -> datetime.timedelta:
    return duration_mapping.get(duration_from_form)
