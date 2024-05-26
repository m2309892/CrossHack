import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_data_from_forms(spreadsheet_name):
    """
    Определение списка разрешений для доступа к данным Google Sheets,
    credentials и авторизация по ним,
    открытие гугл-таблицы с ответами на форму
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).sheet1

    # Возвращаем список данных
    return sheet.get_all_records()


# Пример использования
print(get_data_from_forms("Заявка на проведение лекции (Ответы)"))

[
    {
        "Отметка времени": "25.05.2024 1:07:18",
        "Ваши имя и фамилия": "Анна Кузнецова",
        "Ваш ник в Telegram": "@annakuz",
        "Тема (название) лекции": "Английский язык",
        "Описание лекции": "Разговорная практика и грамматика английского для повседневной жизни",
        "Место проведения": "Только дистанционно",
        "Дата проведения": "24.06.2024 19:00:00",
        "Длительность лекции": "1 час",
        "Дополнительная информация": "",
    },
    {
        "Отметка времени": "25.05.2024 1:08:18",
        "Ваши имя и фамилия": "Павел Смирнов",
        "Ваш ник в Telegram": "@psmirnov",
        "Тема (название) лекции": "Кулинарные хитрости",
        "Описание лекции": "Мастер-класс по приготовлению домашней пасты и соусов",
        "Место проведения": "Румянцево",
        "Дата проведения": "28.06.2024 11:00:00",
        "Длительность лекции": "1,5 часа",
        "Дополнительная информация": "",
    },
]
