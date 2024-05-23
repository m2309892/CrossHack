import telebot
from telebot import types # для указание типов
from html.parser import HTMLParser


admins = [...]  # список ID админов
users = [..., ...]  # список ID сотрудников
TOKEN ='...'

bot = telebot.TeleBot(TOKEN) 

# Приветствие и выбор кнопок 
@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    # Проверка статуса "Сотрудник" или "Админ" или "Никто" 
    # Если "Админ"
    # Админ должен быть в обоих бд, тк он и сотрудник и админ:
    if message.from_user.id in admins and message.from_user.id in users:
        
        markup = types.InlineKeyboardMarkup()

        button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
        button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
        button3 = types.InlineKeyboardButton("Дайджест на неделю", callback_data='digest_for_week')
        button4 = types.InlineKeyboardButton("Отчетнсть лекций за месяц", callback_data='MonthLecRep')
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
        button3 = types.InlineKeyboardButton("Дайджест на неделю", callback_data='digest_for_week')
    
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
        
        # какая тут логика?
        
        
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

    # Если пользователь нажал "Мои лекции"
    if callback.data == 'give_lecture':
        
        # какая тут логика?
        
        
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

    # Если пользователь нажал "Дайджест на неделю"
    if callback.data == 'give_lecture':
        
        # какая тут логика?
        
        bot.send_message(callback.message.chat.id, "Список запланированных лекций:")
        
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.add(button_back)

    # Если пользователь нажал "Отчетность лекций за месяц"
    if callback.data == 'MonthLecRep':
        # какая тут логика?
        bot.send_message(callback.message.chat.id, "Пожалуйста, введите имя сотрудника:")
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
        bot.send_message(callback.message.chat.id, "Выберете нужное действие:", reply_markup=markup)

    elif callback.data == 'resultsForms':
        bot.send_message(callback.message.chat.id, "Список всех действительных опросов:")

    #elif callback.data == 'back':
        

bot.polling(none_stop=True)