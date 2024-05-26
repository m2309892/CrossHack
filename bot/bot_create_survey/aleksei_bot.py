import telebot
import datetime
from telebot import types # для указание типов
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
from html.parser import HTMLParser
from sqlalchemy_engine import Mailing, Session
from workers import get_mailings, add_new_mailing
from converters import convert_date, convert_duration

API_TOKEN = '5471218632:AAFD0hHTx95SRkycWK88QQurUA96LAahbfU'
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scheduler = BackgroundScheduler()
scheduler.start()

# кто подписан на рассылку
subscribers = [318854597,]

# Отправка всем подписчикам из subscribers
def send_notifications(message):
    for user in subscribers:
        try:
            bot.send_message(user, message, parse_mode='HTML')
            logging.info(f"Отправлено уведомление {user}: {message}")
        except Exception as e:
            logging.error(f"Не отправлено уведомление {user}: {e}")

# Планировать уведомления про опросы
def schedule_notify_forms():
    for entry in get_mailings():
        notify_time = datetime.datetime.strptime(entry['date'], '%d.%m.%Y %H:%M:%S')
        # проверка, что надо запланировать уведомление 
        if notify_time > datetime.datetime.now():
            scheduler.add_job(send_notifications, 'date', run_date=notify_time, args=[f"{entry['text']}\nСсылка на <a href='{entry['url']}'>гугл форму</a>"])
            logging.info(f"Запланировано уведомление {entry['mailing_id']} for {notify_time}")

# Планируем по тем формам, что изначально есть в БД
schedule_notify_forms()

# команда старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать. Вы получаете рассылку.")
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    #button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
    button3 = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_week')
    #button4 = types.InlineKeyboardButton("Отчётность лекций за месяц", callback_data='MonthLecRep')
    button5 = types.InlineKeyboardButton("Создать опрос", callback_data='SelecofApplic')
    markup.add(button1)
    #markup.add(button2)
    markup.add(button3)
    #markup.add(button4)
    markup.add(button5)
    bot.send_message(message.chat.id, '<b>Привет, {0.first_name}!</b> Я чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')
    if user_id not in subscribers:
        subscribers.append(user_id)
        logging.info(f"Новый подписчик: UserID={user_id}, FirstName={first_name}, Username={username}")
        print(subscribers)

@bot.callback_query_handler(func=lambda message: True)
def handle_message(callback):
    # Если пользователь нажал "Подбор заявок от спикеров/организаторов"
    if callback.data == 'SelecofApplic':
        # создается новая менюшка
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Создать опрос", callback_data='createForms')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button1)
        markup.add(button_back)
        bot.send_message(callback.message.chat.id, "Выберите нужное действие:", reply_markup=markup)

    # Если пользователь нажал "Создать опрос"
    if callback.data == 'createForms':
        poll_data = {}

        def process_title_step(message):
            poll_data['title'] = message.text
            msg = bot.send_message(message.chat.id, "Напишите текст рассылки (ссылка на форму указывается потом). Пример:\n Добрый день коллеги!\nОткрыта запись на лекции в июне!")
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
            # Оповещаем пользователя об успешном создании опроса
            bot.send_message(message.chat.id, "Опрос успешно создан!")
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
            status = 'Неактивна'
            admin_name = f'@{message.from_user.username}'
            print(session, type, text, survey_url, date, status, admin_name)
            add_new_mailing(session, type, text, survey_url, date, status, admin_name)
            # заново планируем уведомления
            schedule_notify_forms()

        fake_message = callback.message 
        fake_message.text = ""
        process_title_step(fake_message)

# Start polling
while True:
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"Polling error: {e}")
        time.sleep(15)  # Sleep to avoid polling failure issues ??