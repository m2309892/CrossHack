from db.models import Mailing, Lecture, Session, User
from form_api.get_data_from_form import get_data_from_forms
import datetime
from sqlalchemy import update, extract
import logging

# запрос данных из БД
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


def get_lectures():
    session = Session()
    lectures_data = [
        {
            "lecture_id": str(lecture.lecture_id),
            "lecture_name": lecture.lecture_name,
            "lecture_description": lecture.lecture_description,
            "location": lecture.location,
            "date": lecture.date.strftime("%d.%m.%Y %H:%M:%S"),
            "duration": lecture.duration,
            "additional_info": lecture.additional_info if lecture.additional_info else None,
            "tg_username": lecture.tg_username,
            "feedback_url": lecture.feedback_url if lecture.feedback_url else None,
            "conference_url": lecture.conference_url if lecture.conference_url else None,
            "lecture_materials_url": lecture.lecture_materials_url if lecture.lecture_materials_url else None,
            "status": lecture.status if lecture.status else None,
            "time_in_sheet": lecture.time_in_sheet.strftime("%d.%m.%Y %H:%M:%S") if lecture.time_in_sheet else None,
            "tags": lecture.tags if lecture.tags else None,
            "calendar_url": lecture.calendar_url if lecture.calendar_url else None,
        }
        for lecture in session.query(Lecture).all()
    ]
    session.close()
    return lectures_data


"""def get_lectures_for_month(month):
    session = Session()
    month = int(month)
    year = int(year)
    lectures_data_monthly = [
        {
            "lecture_id": str(lecture.lecture_id),
            "lecture_name": lecture.lecture_name,
            "lecture_description": lecture.lecture_description,
            "location": lecture.location,
            "date": lecture.date.strftime("%d.%m.%Y %H:%M:%S"),
            "duration": lecture.duration,
            "additional_info": lecture.additional_info if lecture.additional_info else None,
            "tg_username": lecture.tg_username,
            "feedback_url": lecture.feedback_url if lecture.feedback_url else None,
            "conference_url": lecture.conference_url if lecture.conference_url else None,
            "lecture_materials_url": lecture.lecture_materials_url if lecture.lecture_materials_url else None,
            "status": lecture.status if lecture.status else None,
            "time_in_sheet": lecture.time_in_sheet.strftime("%d.%m.%Y %H:%M:%S") if lecture.time_in_sheet else None,
            "tags": lecture.tags if lecture.tags else None,
            "calendar_url": lecture.calendar_url if lecture.calendar_url else None,
        }
        for lecture in session.query(Lecture).filter(
            func.extract('month', Lecture.date) == month,
            func.extract('year', Lecture.date) == year
        ).all()
    ]
    session.close()
    return lectures_data_monthly"""


def get_subscribers():
    session = Session()
    subscribers = [
        {
            "tg_username":user.tg_username,
            "tg_id":user.tg_chat_id,
            "name":user.name,
            "status_user":user.status_user,
        }
        for user in session.query(User).all() if user.status_user in ["Админ", "Работает"]
    ]
    session.close()
    return subscribers


def get_active_mailings():
    session = Session()
    active_lectures = [
        {
            "text":mailing.text,
            "url":mailing.survey_url,
        }
        for mailing in session.query(Mailing).all() if mailing.status == 'Активна'
    ]  
    session.close()
    return active_lectures


def add_new_mailing(session, type, text, survey_url, date, status, admin_name, deadline):
    # Create a new Mailing instance
    new_mailing = Mailing(
        type=type,
        text=text,
        survey_url=survey_url,
        date=date,
        status=status,
        admin_name=admin_name,
        deadline=deadline,
    )
    # Add the new mailing to the session
    session.add(new_mailing)
    # Commit the transaction
    session.commit()
    logging.info(f"Добавлена новая рассылка на {date}")


def add_or_update_lecture(session, data):

    time_in_sheet = datetime.datetime.strptime(data.get('Отметка времени'), "%d.%m.%Y %H:%M:%S")
    
    # Check if a lecture with the same timestamp already exists
    existing_lecture = session.query(Lecture).filter(Lecture.time_in_sheet == time_in_sheet).first()
    
    if existing_lecture:
        pass
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
        logging.info(f"Лекция {data.get('Тема (название) лекции')} успешно добавлена")
    
    session.commit()


def add_lectures_from_sheets(spreadsheet_name):
    session = Session()
    logging.info(f'Запрос ответов из гугл формы {spreadsheet_name}')
    data = get_data_from_forms(spreadsheet_name)
    for entry in data:
        add_or_update_lecture(session, entry)


def update_user_id(tg_username, tg_userid):
    session = Session()
    user = session.query(User).filter_by(tg_username=tg_username).first()
    logging.info(f'Обнаружен сотрудник c {tg_username}, заносится его id в БД')
    user.tg_chat_id = tg_userid
    session.commit()
    session.close()


def get_subscribers_id():
    subscribers_with_id = []
    for subscriber in get_subscribers():
        if subscriber['tg_id']:
            subscribers_with_id.append(subscriber['tg_id'])
    return subscribers_with_id


def get_subscribers_username():
    subscribers_with_id = []
    for subscriber in get_subscribers():
        if subscriber['tg_username']:
            subscribers_with_id.append(subscriber['tg_username'])
    return subscribers_with_id


def check_if_admin(tg_userid):
    session = Session()
    user = session.query(User).filter_by(tg_chat_id=tg_userid).first()
    
    if user is None:
        logging.info(f"Проверка админа: пользователь с {tg_userid} не обнаружен")
        session.close()
        return False
    
    if user.status_user == "Админ":
        logging.info(f"Проверка админа: пользователь с {tg_userid} это админ")
        session.close()
        return True
    
    session.close()
    return False


def check_if_has_access(tg_userid, tg_username):
    session = Session()
    user = session.query(User).filter(
        (User.tg_chat_id == tg_userid) | (User.tg_username == tg_username)
    ).filter(User.status_user.in_(["Админ", "Работает"])).first()
    
    session.close()
    
    if user:
        return True
    else:
        return False


def check_mailing_status():
    session = Session()
    mailings = session.query(Mailing).all()

    for mailing in mailings:
        if mailing.status == 'Неактивна' and mailing.date <= datetime.datetime.now():
            # Если уже разослана, она активна
            session.execute(update(Mailing).where(Mailing.mailing_id == mailing.mailing_id).values(status='Активна'))
        elif mailing.status == 'Активна' and datetime.datetime.now() <= mailing.date:
            # Если она будет разослана позже, она должна быть неактивна
            session.execute(update(Mailing).where(Mailing.mailing_id == mailing.mailing_id).values(status='Неактивна'))
        elif mailing.status == 'Активна' and mailing.deadline <= datetime.datetime.now():
            # Становится неавтина после дэдлайна
            session.execute(update(Mailing).where(Mailing.mailing_id == mailing.mailing_id).values(status='Неактивна'))
    session.commit()
    print("Проверены статусы рассылок.")
    session.close()
    
    
#получить лекции текущего месяца
def get_lectures_of_month():
    session = Session()
    
    # Get current month and year
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    # Query lectures for the current month
    lectures = session.query(Lecture).filter(
        extract('month', Lecture.date) == current_month,
        extract('year', Lecture.date) == current_year,
        Lecture.status == 'Запланирована'
    ).all()
    
    lectures_data = [
        {
            "lecture_id": str(lecture.lecture_id),
            "lecture_name": lecture.lecture_name,
            "lecture_description": lecture.lecture_description,
            "location": lecture.location,
            "date": lecture.date.strftime("%d.%m.%Y %H:%M:%S"),
            "duration": lecture.duration,
            "additional_info": lecture.additional_info if lecture.additional_info else None,
            "tg_username": lecture.tg_username,
            "feedback_url": lecture.feedback_url if lecture.feedback_url else None,
            "conference_url": lecture.conference_url if lecture.conference_url else None,
            "lecture_materials_url": lecture.lecture_materials_url if lecture.lecture_materials_url else None,
            "status": lecture.status if lecture.status else None,
            "time_in_sheet": lecture.time_in_sheet.strftime("%d.%m.%Y %H:%M:%S") if lecture.time_in_sheet else None,
            "tags": lecture.tags if lecture.tags else None,
            "calendar_url": lecture.calendar_url if lecture.calendar_url else None,
        }
        for lecture in lectures
    ]
    
    session.close()
    return lectures_data