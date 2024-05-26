import telebot
from telebot import types # для указание типов
from datetime import datetime
from html.parser import HTMLParser

from src.db.config import config
from workes import *
from src.db.schemas import *


TOKEN = config.bot_token

#вместо этого воркеры для проверок:

'''admins = [...]  # список ID админов
users = [..., ...]  # список ID сотрудников
urlFormID = ... # ССЫЛКА НА ФОРМУ "ПРОВЕСТИ ЛЕКЦИЮ"

# ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ ПРОВЕРЯЕТ АДМИН ТЫ ИЛИ НЕТ
global global_var
global_var = False  # Создание глобальной переменной типа boolean со значением False

# Изменение значения переменной на True (ЕСЛИ АДМИНКА ЕСТЬ)
def change_global_var_to_true():
    global global_var
    global_var = True'''

#get lections проверка на пустой лист

'''# вместо бд и проверок (ЕСТЬ ЛИ ЛЕКЦИИ)
there_is_a_form = False  # ведётся не ведётся набор'''

#запрос из бд
'''# название кнопок и название лекций
lectures_of_user = ["Разработка", "Маркетинг", "Тестирование", "Обучение"]'''


#запрос к бд 
'''# СОЗДАТЬ ОПРОС
# Хранилище для данных опроса
poll_data = {}
# Список для хранения опросов
poll_list = []'''


bot = telebot.async_telebot(TOKEN) 


def menu_inline_admin_keyboard():    
    # Создаем объект для inline клавиатуры
    markup = types.InlineKeyboardMarkup() # создание inline клавиатуры

    button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
    button3 = types.InlineKeyboardButton("Дайджест на неделю", callback_data='digest_for_week')
    button4 = types.InlineKeyboardButton("Отчётность лекций за месяц", callback_data='MonthLecRep')
    button5 = types.InlineKeyboardButton("Подбор заявок от спикеров/организаторов", callback_data='SelecofApplic')
    markup.add(button1) #переписать в одну строку
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    markup.add(button5)

    return markup

# СОЗДАЕМ МЕНЮ ДЛЯ ЮЗЕРОВ
def menu_inline_user_keyboard():    
    # Создаем объект для inline клавиатуры
    markup = types.InlineKeyboardMarkup() # создание inline клавиатуры

    button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
    button3 = types.InlineKeyboardButton("Дайджест на неделю", callback_data='digest_for_week')
    
    markup.add(button1) #переписать в одну строку
    markup.add(button2)
    markup.add(button3)


    return markup


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
async def handle_back_to_menu(message):
    # ЕСЛИ АДМИН
    if check_admin(message.from_user.username):
        markup = menu_inline_admin_keyboard() # создание inline клавиатуры c основным меню
        await bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)
    # ЕСЛИ СОТРУДНИК
    else:
        markup = menu_inline_user_keyboard() # создание inline клавиатуры c основным меню
        await bot.send_message(message.chat.id, 'Вы вернулись в главное меню!', reply_markup=markup)


# Приветствие и выбор кнопок 
@bot.message_handler(commands=['start']) #создаем команду
async def start(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    # Проверка статуса "Сотрудник" или "Админ" или "Никто" 
    # Если "Админ"
    # Админ должен быть в обоих бд, тк он и сотрудник и админ:
    if check_admin(username): #check admin
        
        '''# Вызов функции для изменения значения переменной
        change_global_var_to_true()'''

        markup = types.InlineKeyboardMarkup()
        
        button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
        button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
        button3 = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_week')
        button4 = types.InlineKeyboardButton("Отчётность лекций за месяц", callback_data='MonthLecRep')
        button5 = types.InlineKeyboardButton("Подбор заявок от спикеров/организаторов", callback_data='SelecofApplic')
        markup.add(button1, button2, button3, button4, button5) #переписать в одну строку

        await bot.send_message(message.chat.id, '<b>Привет, {first_name}!</b> Я чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')

    # Если "Сотрудник"
    elif check_user(username):
        markup = types.InlineKeyboardMarkup()

        button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
        button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
        button3 = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_week')
    
        markup.add(button1, button2, button3) #переписать в одну строку

        await bot.send_message(message.chat.id, '<b>Привет, {first_name}!</b> Я чат-бот для образовательных мероприятий компании. Предоставляю сотрудникам возможность получать  уведомления о готовящихся лекциях и Crosstalks. Помогу быть в курсе актуальных событий и планировать свое участие заранее. Для дальнейших действий - нажимай на нужную кнопку!)'.format(message.from_user), reply_markup=markup, parse_mode='html')

    # Если не админ и не сотрудник
    else:
        await bot.send_message(message.chat.id, '<b>Привет, {first_name}!</b> К сожалению, Вы не можете пользоваться данным ботом. Так как не являетесь сотрудником компании.'.format(message.from_user),  parse_mode='html')

# обработчики кнопок
@bot.callback_query_handler(func=lambda message: True)
async def handle_message(callback): #помогите с логикой тут уже, написала функи, дергающие мэйлинги по фильтрам
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    # Если пользователь нажал "Провести лекцию"
    if callback.data == 'give_lecture':

        '''# Переменная, содержащая название месяца (например, "июнь" или "август")
        month = "июнe"

        # Переменная, содержащая мероприятие (лекция или CrossTalks)
        CROSSevent = "лекцию"'''
        mailing_lecture_list = get_mailing_filter(StatusMailing('Активен'), MailType('Лекция'))
        if len(mailing_lecture_list) == 1:
            CROSSevent = mailing_lecture_list[0].text
        mailing_crosstalks_list = get_mailing_filter(StatusMailing('Активен'), MailType('CrossTalks')) #я не ебу, что по модели пайдантика тут указывать, честно, затвра спрошу у шарящих людей, это какой-то пиздец
        if len(mailing_crosstalks_list) == 1:
            CROSSevent = mailing_lecture_list[0].text
        
        markup = types.InlineKeyboardMarkup()
        buttonLecture = types.InlineKeyboardButton(text='Провести лекцию', callback_data='urlForm') #get_current_mailing + проверка статуса
        buttonCrossTalks = types.InlineKeyboardButton(text='Провести CrossTalks', callback_data='urlForm') #get_current_mailing + проверка статуса
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(buttonLecture)
        markup.add(buttonCrossTalks)
        markup.add(button_back)


        await bot.send_message(callback.message.chat.id, "<b>Добрый день, коллеги!</b>\n\nОткрыта запись на <b>{CROSSevent}</b> в {month}\n\nНажимайте на <b>Провести лекцию</b> для получения ссылки на гугл форму".format(CROSSevent=CROSSevent, month=month), reply_markup=markup, parse_mode='html')
        

    # Если пользователь нажал "Мои лекции"
    if callback.data == 'my_lecture':

        markup = types.InlineKeyboardMarkup()
        
        #накинуть проверку на пустоту листа
        lectures_of_user = get_lectures_by_tg(username)
        if lectures_of_user is None:
            await bot.send_message(callback.message.chat.id, "Пока у вас нет лекций")
        else:
            for user_lection in lectures_of_user: #get_user_lections
                button = types.InlineKeyboardButton(
                   f'Лекция "{user_lection}"', callback_data=user_lection
                )
                markup.add(button)

                button_back = types.InlineKeyboardButton("Назад", callback_data='back')
                markup.add(button_back)
                
                await bot.send_message(
                    callback.message.chat.id,
                    "Мои лекции.\nВыберите нужное действие:",
                    reply_markup=markup,
                    parse_mode="html",
                )

    # Если пользователь нажал "Дайджест на месяц"
    if callback.data == 'digest_for_week':
    
        # Условная БД -- неусловный метод get_digest
        events = get_all_lectures(StatusLecture('Одобрена'))

        # Фильтрация мероприятий со статусом "будет"   ДВЕ ФИЛЬТРАЦИИ ПО ДАТЕ И ПО СТАТУСУ
        #events = [event for event in events if event['status'] == 'будет']

        # Сортировка по дате
        events = sorted(events, key=lambda x: x['date']) #сука я не понимаю, как это сделать бляяя

        markup = types.InlineKeyboardMarkup()
        buttonback = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(buttonback)
    
        msg = "<b>Мы подготовили дайджест событий на этот месяц:</b>\n\n"
        for event in events:
            msg += f"{event['date']} - {event['name']}\n"  # Статус больше не нужен, так как все события будут со статусом "будет"

        await bot.send_message(callback.message.chat.id, msg, reply_markup=markup, parse_mode='html')

    # Если пользователь нажал "Отчетность лекций за месяц"
    if callback.data == 'MonthLecRep':
        
        # Отправляем запрос на ввод телеграм-username сотрудника
        msg = bot.send_message(callback.message.chat.id, "Пожалуйста, введите телеграм-username сотрудника:")
    
        # Создаем обработчик для ответа пользователя
        @bot.message_handler(content_types=['text'])
        async def handle_employee_username(message):
            if message.chat.id == callback.message.chat.id:
                employee_username = message.text
            
                # Имитация базы данных функция get_user_lections
                '''lectures = [
                    {'employee_username': '@john_doe', 'lecture_name': 'Лекция 1', 'lecture_date': '10.07.2024'},
                    {'employee_username': '@john_doe', 'lecture_name': 'Лекция 2', 'lecture_date': '15.07.2024'},
                    {'employee_username': '@jane_smith', 'lecture_name': 'Лекция 3', 'lecture_date': '20.07.2024'}
                ]  '''
                employee_lectures = get_lectures_by_tg(employee_username) 
            
                # Фильтруем лекции по введенному телеграм-username сотрудника
                #employee_lectures = [lecture for lecture in lectures if lecture['employee_username'] == employee_username]
            
                # Формируем сообщение с отчетностью
                report_message = "<b>Отчетность лекций за месяц:</b>\n\n"
                for lecture in employee_lectures:
                    report_message += f"Название лекции: {lecture.lecture_name}\nДата проведения: {lecture.lecture_date}\n\n"

                markup = types.InlineKeyboardMarkup()
                buttonback = types.InlineKeyboardButton("Назад", callback_data='back')
                markup.add(buttonback)

                # Отправляем сообщение с отчетностью
                await bot.send_message(callback.message.chat.id, report_message, reply_markup=markup, parse_mode='html')
            

    # Если пользователь нажал "Подбор заявок от спикеров/организаторов"
    if callback.data == 'SelecofApplic':
        # создается новая менюшка
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Создать опрос", callback_data='createForms')
        button2 = types.InlineKeyboardButton("Посмотреть результаты опроса", callback_data='resultsForms') #пока убираем
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button1)
        markup.add(button2)
        markup.add(button_back)
        await bot.send_message(callback.message.chat.id, "Выберите нужное действие:", reply_markup=markup)

    # Если пользователь нажал "Создать отпрос"
    if callback.data == 'createForms':
        # Состояния
        STATE_TITLE, STATE_MESSAGE, STATE_LINK, STATE_SEND_DATE, STATE_DEADLINE = range(5)

        poll_data = {}
        async def process_title_step(message):
            poll_data['title'] = message.text
            msg = await bot.send_message(message.chat.id, "Напишите текст рассылки. Пример: Добрый день коллеги! Открыта запись на лекции в июне!")
            await bot.register_next_step_handler(msg, process_message_step)

        async def process_message_step(message):
            poll_data['message'] = message.text
            msg = await bot.send_message(message.chat.id, "Напишите ссылку на гугл форму.")
            await bot.register_next_step_handler(msg, process_link_step)

        async def process_link_step(message):
            poll_data['link'] = message.text
            msg = await bot.send_message(message.chat.id, "Напишите дату и время рассылки. Пример: 2024-05-25 9:00")
            await bot.register_next_step_handler(msg, process_send_date_step)

        async def process_send_date_step(message):
            poll_data['send_date'] = message.text
            msg = await bot.send_message(message.chat.id, "Напишите дедлайн опроса. Пример: 2024-06-10 18:00")
            await bot.register_next_step_handler(msg, process_deadline_step)

        async def process_deadline_step(message):
            poll_data['deadline'] = message.text

            # Здесь сохраняем данные в список или обрабатываем иначе по логике
            #create mailing
            create_mailing(poll_data.copy())
            '''poll_list.append(poll_data.copy())  # Добавляем в список опросов '''
            # Оповещаем пользователя об успешном создании опроса
            await bot.send_message(message.chat.id, "Опрос успешно создан!")
            # Показываем введенные данные
            summary = (f"Название опроса: {poll_data['title']}\n"
                        f"Текст рассылки: {poll_data['message']}\n"
                        f"Ссылка на гугл форму: {poll_data['link']}\n"
                        f"Дата и время рассылки: {poll_data['send_date']}\n"
                        f"Дедлайн опроса: {poll_data['deadline']}")
            
            await bot.send_message(message.chat.id, summary)

        msg = await bot.send_message(callback.message.chat.id, "Пожалуйста, введите название опроса:")
        await bot.register_next_step_handler(msg, process_title_step) #какая-то хуита

    
    elif callback.data == 'back':
        
        # УДАЛЯЕМ СООБЩЕНИЕ
        #bot.delete_message(callback.message.chat.id, callback.message.message_id)

        handle_back_to_menu(callback.message)
        

    # Если пользователь нажал копку "Посмотреть результаты опроса"
    elif callback.data == 'resultsForms':
        await bot.send_message(callback.message.chat.id, "Список всех действительных опросов:")

    # Если пользователь нажал копку "Провести лекции"
    elif callback.data == 'urlForm':
        if : #check status mailings
            # присылается ссылка на гугл форму 
            await bot.send_message(callback.message.chat.id, "Отлично! Вот ссылка на <a href='https://forms.gle/u2K5frepjugeZq8j8'>гугл</a>.", parse_mode='HTML')
        else:
            # присылается грустное сообщение 
            await bot.send_message(callback.message.chat.id, "Запись не ведётся сейчас:(\nСледите за уведомлениями в этом боте, Вам обязательно напишут, когда появится гугл форма", parse_mode='HTML')

    # МОИ ЛЕКЦИИ (Инфа о них)
    elif callback.data in lectures_of_user: #get_lection_by_id
            
        '''# ТИПА БД
        lecture_id = 1
        name = ''
        day = '10/10/2025'
        time = '10:00'
        call_link = 'что-то...'
        status = 'будет'''
        lecture_data = callback.data
        
        markup = types.InlineKeyboardMarkup()

        # присылается сообщение с информацией из БД 
        message = f"ID лекции: {lecture_data.id}\nНазвание: {name}\nДата: {day}\nВремя: {time}\nСсылка для подключения: {call_link}\nСтатус: {status}"
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

        await bot.send_message(
            callback.message.chat.id,
            message,
            reply_markup=markup,
            parse_mode="html",
        )

        

bot.polling(none_stop=True)