import telebot
import datetime
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
from html.parser import HTMLParser
from sqlalchemy_engine import Session
from workers import get_mailings, get_lectures, add_new_mailing, update_user_id, get_subscribers, get_subscribers_id, check_if_admin, check_if_has_access, add_lectures_from_sheets, check_mailing_status, get_active_mailings
from converters import convert_date, convert_duration
import threading
from main_menu_buttons import menu_inline_admin_keyboard, menu_inline_user_keyboard

API_TOKEN = '5471218632:AAFD0hHTx95SRkycWK88QQurUA96LAahbfU'
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scheduler = BackgroundScheduler()
scheduler.start()

admin_creating_survey = {}
# Отправка всем, кто имеет доступ к боту
def send_notifications(message):
    for user in get_subscribers_id():
        print(get_subscribers_id())
        try:
            bot.send_message(user, message, parse_mode='HTML')
            logging.info(f"Отправлено уведомление {user}: {message}")
        except Exception as e:
            logging.error(f"Не отправлено уведомление {user}: {e}")

# Планировать уведомления про опросы (опрос = сообщение с приглашением пройти гугл форму)
def schedule_notify_forms():
    logging.info("Планирутся опросы...")
    for entry in get_mailings():
        notify_time = datetime.datetime.strptime(entry['date'], '%d.%m.%Y %H:%M:%S')
        # проверка, что надо запланировать уведомление 
        if notify_time > datetime.datetime.now():
            scheduler.add_job(send_notifications, 'date', run_date=notify_time, args=[f"{entry['text']}\nСсылка на <a href='{entry['url']}'>гугл форму</a>"])
            logging.info(f"Запланировано уведомление для опроса на {notify_time}")

# Планировать уведомления про лекции
def schedule_notify_lectures():
    logging.info("Планирутся лекции...")
    for lecture in get_lectures():
        status = (lecture['status'])
        if status == 'Запланирована':
            lecture_start = datetime.datetime.strptime(lecture['date'], '%d.%m.%Y %H:%M:%S')
            lecture_end = lecture_start + convert_duration(lecture['duration'])
            lecture_start_str = lecture_start.strftime('%d.%m c %H:%M до ')
            lecture_end_str = lecture_end.strftime('%H:%M')
            lecture_period = f'{lecture_start_str}{lecture_end_str}'

            # проверка, что надо запланировать уведомление 
            if lecture_start > datetime.datetime.now():
                notification = f"О запланированной лекции!\n🗓️ <a href='{lecture['calendar_url']}'>{lecture_period}</a> пройдёт лекция <b>{lecture['lecture_name']}</b>\n{lecture['lecture_description']}\n\n🥸 Лекционную часть проведёт {lecture['tg_username']}\n📍 Лекция проводится {lecture['location']}, ссылка на google meet: {lecture['conference_url']}\nМатериалы будут доступны после мини-лекции <a href='{lecture['lecture_materials_url']}'>ВОТ ТУТ</a>\n{lecture['tags']}"
                notification_times = [
                    lecture_start - datetime.timedelta(days=7),
                    lecture_start - datetime.timedelta(days=3),
                    lecture_start.replace(hour=9, minute=0, second=0, microsecond=0),
                    lecture_start - datetime.timedelta(minutes=5)
                ]
                count_notifications = 0
                for notify_time in notification_times:
                    if notify_time > datetime.datetime.now():
                        scheduler.add_job(send_notifications, 'date', run_date=notify_time, args=[notification])
                        count_notifications+=1
                logging.info(f"Созданы уведомления ({count_notifications}) для лекции {lecture['lecture_name']}")

# команда /старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = f"@{message.from_user.username}"
    if check_if_has_access(user_id,username):
        subscribers_ids = [user['tg_id'] for user in get_subscribers()]
        subscribers_usernames =  [user['tg_username'] for user in get_subscribers()]
        if username in subscribers_usernames:
            if user_id not in subscribers_ids:
                update_user_id(username, user_id)
        markup = menu_inline_user_keyboard()
        if check_if_admin(user_id):
            logging.info(f'{username} - админ')
            markup = menu_inline_admin_keyboard()
        else: 
            logging.info(f'{username} - обычный пользователь')
        bot.send_message(message.chat.id, f'<b>Привет, {first_name}!</b>\nЯ чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'Нет доступа')
        logging.info(f'{username} пробует зайти в бот')

@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_back_to_menu(message):
    user_id = message.chat.id
    # ЕСЛИ АДМИН
    if check_if_admin(user_id):
        markup = menu_inline_admin_keyboard() # создание inline клавиатуры c основным меню
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)
    # ЕСЛИ СОТРУДНИК
    else:
        markup = menu_inline_user_keyboard() # создание inline клавиатуры c основным меню
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)

# обрабатываем кнопки
@bot.callback_query_handler(func=lambda message: True)
def handle_message(callback):
    # Если пользователь нажал "Создать опрос"
    if callback.data == 'create_survey':
        # создается новая менюшка
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Создать опрос", callback_data='createForms')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button1)
        markup.add(button_back)
        bot.send_message(callback.message.chat.id, "Выберите нужное действие:", reply_markup=markup)

    # Если пользователь нажал "Создать опрос"
    if callback.data == 'createForms':
        user_id = callback.from_user.id
        if check_if_admin(user_id):
            if user_id in admin_creating_survey:
                bot.send_message(callback.message.chat.id, 'Вы уже создаете опрос. Пожалуйста, завершите текущий процесс перед созданием нового опроса.')
                return
            admin_creating_survey[user_id] = True
            poll_data = {}
            def process_title_step(message):
                poll_data['title'] = message.text
                msg = bot.send_message(message.chat.id, "Напишите текст рассылки (ссылка на форму указывается потом). Пример:\nДобрый день коллеги!\nОткрыта запись на лекции в июне!")
                bot.register_next_step_handler(msg, process_message_step)

            def process_message_step(message):
                poll_data['message'] = message.text
                msg = bot.send_message(message.chat.id, "Напишите ссылку на гугл форму.")
                bot.register_next_step_handler(msg, process_link_step)

            def process_link_step(message):
                poll_data['link'] = message.text
                msg = bot.send_message(message.chat.id, "Напишите дату и время рассылки. Пример:\n20.06.2024 14:00:00")
                bot.register_next_step_handler(msg, process_send_date_step)

            def process_send_date_step(message):
                poll_data['send_date'] = message.text
                msg = bot.send_message(message.chat.id, "Напишите дедлайн опроса. Пример:\n20.06.2024 14:00:00")
                bot.register_next_step_handler(msg, process_deadline_step)

            def process_deadline_step(message):
                poll_data['deadline'] = message.text
                # Показываем введенные данные
                summary = (f"Текст рассылки: {poll_data['message']}\n"
                        f"Ссылка на гугл форму: {poll_data['link']}\n"
                        f"Дата и время рассылки: {poll_data['send_date']}\n"
                        f"Дедлайн опроса: {poll_data['deadline']}")
                bot.send_message(message.chat.id, summary)

                session = Session()
                type = 'Лекция'
                text=poll_data['message']
                survey_url=poll_data['link']
                date= datetime.datetime.strptime(poll_data['send_date'], '%d.%m.%Y %H:%M:%S')
                deadline = datetime.datetime.strptime(poll_data['deadline'], '%d.%m.%Y %H:%M:%S')
                print(date, deadline, convert_date(poll_data['send_date']), convert_date(poll_data['deadline']))
                status = 'Неактивна'
                admin_name = f'@{message.from_user.username}'
                add_new_mailing(session, type, text, survey_url, date, status, admin_name, deadline)
                # заново планируем уведомления
                schedule_notify_forms()

            fake_message = callback.message 
            fake_message.text = ""
            process_title_step(fake_message)
        else:
            bot.send_message(callback.message.chat.id, 'Вы больше не админ ДОСТУП ЗАПРЕЩЁН')
    # Если пользователь нажал провести лекцию
    if callback.data == 'give_lecture':
        if get_active_mailings():
            markup = types.InlineKeyboardMarkup()
            buttonForm = types.InlineKeyboardButton(text='Посмотреть гугл формы', callback_data='give_actual_mailings')
            button_back = types.InlineKeyboardButton("Назад", callback_data='back')
            markup.add(buttonForm)
            markup.add(button_back)
            bot.send_message(callback.message.chat.id, 'Сейчас выдётся набор напроведение лекций/участие в CrossTalks:', reply_markup=markup)
        else: 
            bot.send_message(callback.message.chat.id, 'На данный момент нет набора ни на лекции, ни на CrossTalks')

    if callback.data == 'give_actual_mailings':
        message_with_mailings = "Сейчас доступны следующие гугл формы:"
        print(get_active_mailings())
        for mailing in get_active_mailings():
            message_with_mailings+=f"\n{mailing['text']}\n{mailing['url']}"
            print(message_with_mailings)
        print(message_with_mailings)
        bot.send_message(callback.message.chat.id, message_with_mailings)
    elif callback.data == 'back':
        
        # УДАЛЯЕМ СООБЩЕНИЕ
        #bot.delete_message(callback.message.chat.id, callback.message.message_id)

        handle_back_to_menu(callback.message)


        

# Function to periodically check for changes in the database and update notifications
def update_notifications_periodically():
    while True:
        scheduler.remove_all_jobs()
        schedule_notify_forms()
        schedule_notify_lectures()
        add_lectures_from_sheets("Заявка на проведение лекции (Ответы)")
        check_mailing_status()
        time.sleep(30)

# Start a separate thread to run the periodic checking function
update_thread = threading.Thread(target=update_notifications_periodically)
update_thread.daemon = True  # Set the thread as a daemon so it automatically exits when the main program exits
update_thread.start()

# Bot polling loop (main program)
while True:
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"Polling error: {e}")
        time.sleep(15)  # Sleep to avoid polling failure issues
