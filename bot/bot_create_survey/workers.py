from sqlalchemy_engine import Mailing, Lecture, Session
from get_data_from_form import get_data_from_forms
import datetime

def get_mailings():
    session = Session()

    # Fetch data from database
    notifications_data = [
        {
            "mailing_id": str(mailing.mailing_id),
            "type": mailing.type,
            "date": mailing.date.strftime("%d.%m.%Y %H:%M:%S"),
            "text": mailing.text,
            "url": mailing.survey_url,
        }
        for mailing in session.query(Mailing).all()
    ]
    session.close()
    return notifications_data

def add_new_mailing(session, type, text, survey_url, date, status, admin_name):
    # Create a new Mailing instance
    new_mailing = Mailing(
        type=type,
        text=text,
        survey_url=survey_url,
        date=date,
        status=status,
        admin_name=admin_name
    )
    # Add the new mailing to the session
    session.add(new_mailing)
    # Commit the transaction
    session.commit()
    print(f"Добавлена новая рассылка")

def add_or_update_lecture(session, data):

    time_in_sheet = datetime.datetime.strptime(data.get('Отметка времени'), "%d.%m.%Y %H:%M:%S")
    
    # Check if a lecture with the same timestamp already exists
    existing_lecture = session.query(Lecture).filter(Lecture.time_in_sheet == time_in_sheet).first()
    
    if existing_lecture:
        print("Лекция уже существует в БД.")
    else:
        # Add a new lecture to the database
        lecture = Lecture(
            lecture_name=data.get("Тема (название) лекции"),
            lecture_description=data.get("Описание лекции"),
            location=data.get("Место проведения"),
            date=datetime.datetime.strptime(data.get("Дата проведения"), "%d.%m.%Y %H:%M:%S"),
            duration=data.get("Длительность лекции"),
            additional_info=data.get("Дополнительная информация"),
            tg_username=data.get("Ваш ник в Telegram"),
            time_in_sheet=time_in_sheet,
            feedback_url=None,
            conference_url=None,
            lecture_materials_url=None,
            status='На рассмотрении'
        )
        session.add(lecture)
        print("Лекция успешно добавлена")
    
    session.commit()

def add_lectures_from_sheets(spreadsheet_name):
    session = Session()
    data = get_data_from_forms(spreadsheet_name)
    for entry in data:
        add_or_update_lecture(session, entry)
