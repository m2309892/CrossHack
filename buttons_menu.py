from telebot import types  # для указание типов

# СОЗДАЕМ МЕНЮ ДЛЯ АДМИНОВ
def menu_inline_admin_keyboard():    
    # Создаем объект для inline клавиатуры
    markup = types.InlineKeyboardMarkup() # создание inline клавиатуры

    button1 = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    button2 = types.InlineKeyboardButton("Мои лекции", callback_data='my_lecture')
    button3 = types.InlineKeyboardButton("Дайджест на неделю", callback_data='digest_for_week')
    button4 = types.InlineKeyboardButton("Отчётность лекций за месяц", callback_data='MonthLecRep')
    button5 = types.InlineKeyboardButton("Подбор заявок от спикеров/организаторов", callback_data='SelecofApplic')
    markup.add(button1)
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
    
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)


    return markup

