from telebot import types

# СОЗДАЕМ МЕНЮ ДЛЯ АДМИНОВ
def menu_inline_admin_keyboard():    
    markup = types.InlineKeyboardMarkup()
    give_lecture_button = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    digest_for_month_button = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_month')
    markup.add(give_lecture_button, digest_for_month_button)
    create_survey_button = types.InlineKeyboardButton("Создать опрос", callback_data='create_survey')
    markup.add(create_survey_button )

    return markup

# СОЗДАЕМ МЕНЮ ДЛЯ ЮЗЕРОВ
def menu_inline_user_keyboard():    
    markup = types.InlineKeyboardMarkup()
    give_lecture_button = types.InlineKeyboardButton("Провести лекцию", callback_data='give_lecture')
    digest_for_month_button = types.InlineKeyboardButton("Дайджест на месяц", callback_data='digest_for_month')
    markup.add(give_lecture_button, digest_for_month_button)

    return markup