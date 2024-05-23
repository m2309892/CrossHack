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
# print(get_data_from_forms("Заявка на проведение лекции (Ответы)"))