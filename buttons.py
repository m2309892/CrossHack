import telebot
from telebot import types # для указание типов
from html.parser import HTMLParser


admins = [...]  # список ID админов
TOKEN ='...'

bot = telebot.TeleBot(TOKEN) 

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    if message.from_user.id in admins:
        
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
        bot.send_message(message.chat.id, '<b>Привет, {0.first_name}!</b> Для дальнейших действий - нажимай на нужную кнопку)'.format(message.from_user), reply_markup=markup, parse_mode='html')
        
# обработчики кнопок
@bot.callback_query_handler(func=lambda message: True)
def handle_message(callback):
    # Если пользователь нажал "Провести лекцию"
    if callback.data == 'give_lecture':
        # какая тут логика?
        bot.send_message(callback.message.chat.id,  "Просто текст")

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
        markup.add(button1)
        markup.add(button2)
        bot.send_message(callback.message.chat.id, "Выберете нужное действие:", reply_markup=markup)

bot.polling(none_stop=True)