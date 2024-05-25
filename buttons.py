import telebot
from telebot import types # для указание типов
from datetime import datetime
from html.parser import HTMLParser
from buttons_menu import  menu_inline_admin_keyboard, menu_inline_user_keyboard

TOKEN ='...'

admins = [...]  # список ID админов
users = [..., ...]  # список ID сотрудников
urlFormID = ... # ССЫЛКА НА ФОРМУ "ПРОВЕСТИ ЛЕКЦИЮ"

# ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ ПРОВЕРЯЕТ АДМИН ТЫ ИЛИ НЕТ
global global_var
global_var = False  # Создание глобальной переменной типа boolean со значением False

# Изменение значения переменной на True (ЕСЛИ АДМИНКА ЕСТЬ)
def change_global_var_to_true():
    global global_var
    global_var = True


# вместо бд и проверок (ЕСТЬ ЛИ ЛЕКЦИИ)
there_is_a_form = False  # ведётся не ведётся набор

# название кнопок и название лекций
lectures_of_user = ["Разработка", "Маркетинг", "Тестирование", "Обучение"]


# СОЗДАТЬ ОПРОС
# Хранилище для данных опроса
poll_data = {}
# Список для хранения опросов
poll_list = []




bot = telebot.TeleBot(TOKEN) 

@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_back_to_menu(message):
    # ЕСЛИ АДМИН
    if global_var:
        markup = menu_inline_admin_keyboard() # создание inline клавиатуры c основным меню
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)
    # ЕСЛИ СОТРУДНИК
    else:
        markup = menu_inline_user_keyboard() # создание inline клавиатуры c основным меню
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)


# Приветствие и выбор кнопок 
@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    # Проверка статуса "Сотрудник" или "Админ" или "Никто" 
    # Если "Админ"
    # Админ должен быть в обоих бд, тк он и сотрудник и админ:
    if message.from_user.id in admins and message.from_user.id in users:
        
        # Вызов функции для изменения значения переменной
        change_global_var_to_true()

        markup = types.InlineKeyboardMarkup()
        
        button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
        button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
        button3 = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_week')
        button4 = types.InlineKeyboardButton("Отчётность лекций за месяц", callback_data='MonthLecRep')
        button5 = types.InlineKeyboardButton("Подбор заявок от спикеров/организаторов", callback_data='SelecofApplic')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        markup.add(button5)

        bot.send_message(message.chat.id, '<b>Привет, {0.first_name}!</b> Я чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')

    # Если "Сотрудник"
    elif message.from_user.id in users:
        markup = types.InlineKeyboardMarkup()

        button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
        button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
        button3 = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_week')
    
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)

        bot.send_message(message.chat.id, '<b>Привет, {0.first_name}!</b> Я чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')

    # Если не админ и не сотрудник
    else:
        bot.send_message(message.chat.id, '<b>Привет, {0.first_name}!</b> К сожалению, Вы не можете пользоваться данным ботом. Так как не являетесь сотрудником компании.'.format(message.from_user),  parse_mode='html')

# обработчики кнопок
@bot.callback_query_handler(func=lambda message: True)
def handle_message(callback):
    # Если пользователь нажал "Провести лекцию"
    if callback.data == 'give_lecture':

        # Переменная, содержащая название месяца (например, "июнь" или "август")
        month = "июнe"

        # Переменная, содержащая мероприятие (лекция или CrossTalks)
        CROSSevent = "лекцию"
        
        markup = types.InlineKeyboardMarkup()
        buttonForm = types.InlineKeyboardButton(text='Провести лекцию', callback_data='urlForm')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(buttonForm)
        markup.add(button_back)


        bot.send_message(callback.message.chat.id, "<b>Добрый день, коллеги!</b>\n\nОткрыта запись на <b>{CROSSevent}</b> в {month}\n\nНажимайте на <b>Провести лекцию</b> для получения ссылки на гугл форму".format(CROSSevent=CROSSevent, month=month), reply_markup=markup, parse_mode='html')
        

    # Если пользователь нажал "Мои лекции"
    if callback.data == 'my_lecture':

        markup = types.InlineKeyboardMarkup()

        for user_lection in lectures_of_user:
            button = types.InlineKeyboardButton(
                f'Лекция "{user_lection}"', callback_data=user_lection
            )
            markup.add(button)

        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

        bot.send_message(
            callback.message.chat.id,
            "Мои лекции.\nВыберите нужное действие:",
            reply_markup=markup,
            parse_mode="html",
        )

    # Если пользователь нажал "Дайджест на месяц"
    if callback.data == 'digest_for_week':
    
        # Условная БД
        events = [
            {'date': '10.07.2024', 'status': 'будет', 'name': 'Мероприятие 1'},
            {'date': '10.08.2024', 'status': 'завершено', 'name': 'Мероприятие 2'}
        ]

        # Фильтрация мероприятий со статусом "будет"
        events = [event for event in events if event['status'] == 'будет']

        # Сортировка по дате
        events = sorted(events, key=lambda x: x['date'])

        markup = types.InlineKeyboardMarkup()
        buttonback = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(buttonback)
    
        msg = "<b>Мы подготовили дайджест событий на этот месяц:</b>\n\n"
        for event in events:
            msg += f"{event['date']} - {event['name']}\n"  # Статус больше не нужен, так как все события будут со статусом "будет"

        bot.send_message(callback.message.chat.id, msg, reply_markup=markup, parse_mode='html')

    # Если пользователь нажал "Отчетность лекций за месяц"
    if callback.data == 'MonthLecRep':
        
        # Отправляем запрос на ввод телеграм-username сотрудника
        msg = bot.send_message(callback.message.chat.id, "Пожалуйста, введите телеграм-username сотрудника:")
    
        # Создаем обработчик для ответа пользователя
        @bot.message_handler(content_types=['text'])
        def handle_employee_username(message):
            if message.chat.id == callback.message.chat.id:
                employee_username = message.text
            
                # Имитация базы данных
                lectures = [
                    {'employee_username': '@john_doe', 'lecture_name': 'Лекция 1', 'lecture_date': '10.07.2024'},
                    {'employee_username': '@john_doe', 'lecture_name': 'Лекция 2', 'lecture_date': '15.07.2024'},
                    {'employee_username': '@jane_smith', 'lecture_name': 'Лекция 3', 'lecture_date': '20.07.2024'}
                ]   
            
                # Фильтруем лекции по введенному телеграм-username сотрудника
                employee_lectures = [lecture for lecture in lectures if lecture['employee_username'] == employee_username]
            
                # Формируем сообщение с отчетностью
                report_message = "<b>Отчетность лекций за месяц:</b>\n\n"
                for lecture in employee_lectures:
                    report_message += f"Название лекции: {lecture['lecture_name']}\nДата проведения: {lecture['lecture_date']}\n\n"

                markup = types.InlineKeyboardMarkup()
                buttonback = types.InlineKeyboardButton("Назад", callback_data='back')
                markup.add(buttonback)

                # Отправляем сообщение с отчетностью
                bot.send_message(callback.message.chat.id, report_message, reply_markup=markup, parse_mode='html')
            

    # Если пользователь нажал "Подбор заявок от спикеров/организаторов"
    if callback.data == 'SelecofApplic':
        # создается новая менюшка
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Создать опрос", callback_data='createForms')
        button2 = types.InlineKeyboardButton("Посмотреть результаты опроса", callback_data='resultsForms')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button1)
        markup.add(button2)
        markup.add(button_back)
        bot.send_message(callback.message.chat.id, "Выберите нужное действие:", reply_markup=markup)

    # Если пользователь нажал "Создать отпрос"
    if callback.data == 'createForms':
        # Состояния
        STATE_TITLE, STATE_MESSAGE, STATE_LINK, STATE_SEND_DATE, STATE_DEADLINE = range(5)

        def process_title_step(message):
            poll_data['title'] = message.text
            msg = bot.send_message(message.chat.id, "Напишите текст рассылки. Пример: Добрый день коллеги! Открыта запись на лекции в июне!")
            bot.register_next_step_handler(msg, process_message_step)

        def process_message_step(message):
            poll_data['message'] = message.text
            msg = bot.send_message(message.chat.id, "Напишите ссылку на гугл форму.")
            bot.register_next_step_handler(msg, process_link_step)

        def process_link_step(message):
            poll_data['link'] = message.text
            msg = bot.send_message(message.chat.id, "Напишите дату и время рассылки. Пример: 2024-05-25 9:00")
            bot.register_next_step_handler(msg, process_send_date_step)

        def process_send_date_step(message):
            poll_data['send_date'] = message.text
            msg = bot.send_message(message.chat.id, "Напишите дедлайн опроса. Пример: 2024-06-10 18:00")
            bot.register_next_step_handler(msg, process_deadline_step)

        def process_deadline_step(message):
            poll_data['deadline'] = message.text

            # Здесь сохраняем данные в список или обрабатываем иначе по логике
            poll_list.append(poll_data.copy())  # Добавляем в список опросов
            # Оповещаем пользователя об успешном создании опроса
            bot.send_message(message.chat.id, "Опрос успешно создан!")
            # Показываем введенные данные
            summary = (f"Название опроса: {poll_data['title']}\n"
                        f"Текст рассылки: {poll_data['message']}\n"
                        f"Ссылка на гугл форму: {poll_data['link']}\n"
                        f"Дата и время рассылки: {poll_data['send_date']}\n"
                        f"Дедлайн опроса: {poll_data['deadline']}")
            
            bot.send_message(message.chat.id, summary)

        msg = bot.send_message(callback.message.chat.id, "Пожалуйста, введите название опроса:")
        bot.register_next_step_handler(msg, process_title_step)

    
    elif callback.data == 'back':
        
        # УДАЛЯЕМ СООБЩЕНИЕ
        #bot.delete_message(callback.message.chat.id, callback.message.message_id)

        handle_back_to_menu(callback.message)
        

    # Если пользователь нажал копку "Посмотреть результаты опроса"
    elif callback.data == 'resultsForms':
        bot.send_message(callback.message.chat.id, "Список всех действительных опросов:")

    # Если пользователь нажал копку "Провести лекции"
    elif callback.data == 'urlForm':
        if there_is_a_form:
            # присылается ссылка на гугл форму 
            bot.send_message(callback.message.chat.id, "Отлично! Вот ссылка на <a href='https://forms.gle/u2K5frepjugeZq8j8'>гугл</a>.", parse_mode='HTML')
        else:
            # присылается грустное сообщение 
            bot.send_message(callback.message.chat.id, "Запись не ведётся сейчас:(\nСледите за уведомлениями в этом боте, Вам обязательно напишут, когда появится гугл форма", parse_mode='HTML')

    # МОИ ЛЕКЦИИ (Инфа о них)
    elif callback.data in lectures_of_user:
            
        # ТИПА БД
        lecture_id = 1
        name = ''
        day = '10/10/2025'
        time = '10:00'
        call_link = 'что-то...'
        status = 'будет'
        
        markup = types.InlineKeyboardMarkup()

        # присылается сообщение с информацией из БД 
        message = f"ID лекции: {lecture_id}\nНазвание: {name}\nДата: {day}\nВремя: {time}\nСсылка для подключения: {call_link}\nСтатус: {status}"
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

        bot.send_message(
            callback.message.chat.id,
            message,
            reply_markup=markup,
            parse_mode="html",
        )

        

bot.polling(none_stop=True)