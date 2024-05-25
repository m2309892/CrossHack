import telebot
from telebot import types # для указание типов
from html.parser import HTMLParser
from buttons_menu import  menu_inline_admin_keyboard, menu_inline_user_keyboard

TOKEN ='6527611965:AAEpstUPFSi4SK1qLkDdsjvTuz7X2CkxpUM'

admins = [879863724]  # список ID админов
users = [318854597, 879863724]  # список ID сотрудников
urlFormID = ... # ССЫЛКА НА ФОРМУ "ПРОВЕСТИ ЛЕКЦИЮ"

# ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ ПРОВЕРЯЕТ АДМИН ТЫ ИЛИ НЕТ
global global_var
global_var = False  # Создание глобальной переменной типа boolean со значением False

# Изменение значения переменной на True (ЕСЛИ АДМИНКА ЕСТЬ)
def change_global_var_to_true():
    global global_var
    global_var = True


# вместо бд и проверок
there_is_a_form = True  # ведётся не ведётся набор

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
        
        #   ДОПИСАТЬ ЛОГИКУ, ЕСЛИ ССЫЛКИ НЕТ
        
        markup = types.InlineKeyboardMarkup()

         
        buttonForm = types.InlineKeyboardButton(text='Провести лекцию', callback_data='urlForm')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(buttonForm)
        markup.add(button_back)


        bot.send_message(callback.message.chat.id, "<b>Добрый день, коллеги!</b>\n\nОткрыта запись на <b>{CROSSevent}</b> в {month}\n\nНажимайте на <b>Провести лекцию</b> для получения ссылки на гугл форму".format(CROSSevent=CROSSevent, month=month), reply_markup=markup, parse_mode='html')
        

    # Если пользователь нажал "Мои лекции"
    if callback.data == 'my_lecture':
        
        # какая тут логика?
        # как сделать список лекций в виде кнопок?
        
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)
        bot.send_message(callback.message.chat.id, "<b>Мои лекции.</b>\nВыберите нужное действие:", reply_markup=markup, parse_mode='html')

    # Если пользователь нажал "Дайджест на месяц"
    if callback.data == 'digest_for_week':
        
        # какая тут логика?
        
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        # Кнопка сортировки (по дате)
        butSortDate = types.InlineKeyboardButton("Сортировка по дате", callback_data='back')
        # Кнопка сортировки (по апруву)
        butSortApprove  = types.InlineKeyboardButton("Сортировка по одобрению", callback_data='back')
        markup.add(butSortDate)
        markup.add(butSortApprove)
        markup.add(button_back)
        bot.send_message(callback.message.chat.id, "<b>Дайджест на месяц.</b>\nСписок запланированных лекций:", reply_markup=markup, parse_mode='html')

    # Если пользователь нажал "Отчетность лекций за месяц"
    if callback.data == 'MonthLecRep':

        # какая тут логика?
        bot.send_message(callback.message.chat.id, "Пожалуйста, введите ФИО сотрудника:")

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
        enter_name = ''
        # Обработчик для старта процесса создания опроса
        bot.send_message(callback.message.chat.id, "Для начала введите ваше имя:")
        bot.register_next_step_handler(callback.message, enter_name)

    
    elif callback.data == 'back':
        
        # УДАЛЯЕМ СООБЩЕНИЕ
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

        #handle_back_to_menu(callback.message)
        

    # Если пользователь нажал копку "Посмотреть результаты опроса"
    elif callback.data == 'resultsForms':
        bot.send_message(callback.message.chat.id, "Список всех действительных опросов:")

    # Если пользователь нажал копку "Провести лекции"
    elif callback.data == 'urlForm':
        # присылается ссылка на гугл форму 
        bot.send_message(callback.message.chat.id, "Отлично! Вот ссылка на <a href='https://forms.gle/u2K5frepjugeZq8j8'>гугл</a>.", parse_mode='HTML')

        

bot.polling(none_stop=True)