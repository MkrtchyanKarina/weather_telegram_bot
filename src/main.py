import telebot
from telebot import types

from tokens import bot_token
from parser import current_weather, get_photo

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    markup_reply = types.ReplyKeyboardMarkup()
    button_current_weather = types.InlineKeyboardButton(text="Current weather", callback_data="Current weather")
    button_picture = types.InlineKeyboardButton(text="Beautiful picture of nature", callback_data="Beautiful picture of nature")

    markup_reply.add(button_current_weather, button_picture)
    if message.text in ['/start', 'Hi', 'Hello', 'Привет', 'start', 'hi', 'hello', 'привет']:
        bot.send_message(message.chat.id, "Hello! What do you want?", reply_markup=markup_reply)
        bot.register_next_step_handler(message, answer)
    elif message.text == 'Yes':
        bot.send_message(message.chat.id, "What else do you want? Choose weather or picture: ", reply_markup=markup_reply)
        bot.register_next_step_handler(message, answer)
    elif message.text == "No":
        markup_reply = types.ReplyKeyboardMarkup()
        button_start = types.InlineKeyboardButton(text="start",callback_data="start")
        markup_reply.add(button_start)
        bot.send_message(message.chat.id, "Bye! See you later ))", reply_markup=markup_reply)
        bot.register_next_step_handler(message, start)

    else:
        bot.send_message(message.chat.id, "Sorry, I don't understand what do you mean :(\nPlease, enter your request again: ")


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == "Current weather":
        bot.send_message(message.chat.id, "Ok! Enter your city name: ", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, return_current_weather)
    elif message.text == "Beautiful picture of nature":
        bot.send_message(message.chat.id, "Ok! What you want to see? Text me, please )) ", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, return_beautiful_picture)
    else:
        bot.send_message(message.chat.id, "Sorry, I don't understand what do you mean :(\nPlease, enter your request again: ")
        bot.register_next_step_handler(message, answer)


@bot.message_handler(content_types=["text"])
def continue_(message):
    markup_reply = types.ReplyKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text="Yes", callback_data="Yes")
    button_no = types.InlineKeyboardButton(text="No", callback_data="No")
    markup_reply.add(button_yes, button_no)
    bot.send_message(message.chat.id, "Do you want to continue?", reply_markup=markup_reply)
    bot.register_next_step_handler(message, start)

@bot.message_handler(content_types=["text"])
def return_current_weather(message):
    try:
        photo, text = current_weather(message.text)
        if len(text) == 0 or len(photo) == 0:
            bot.send_message(message.chat.id, "I can't find this city :( \nPlease, write the correct name and try again")
            bot.register_next_step_handler(message, return_current_weather)

        else:
            bot.send_photo(message.chat.id, caption=text, photo=photo)
            continue_(message)
    except:
        bot.send_message(message.chat.id, "Problems with the site :( \nPlease write back later ")
        continue_(message)

@bot.message_handler(content_types=["text"])
def return_beautiful_picture(message):
    photo = get_photo(message.text)
    if len(photo) == 0:
        bot.send_message(message.chat.id, "I can't find this :( \nPlease, write the correct name and try again")
        bot.register_next_step_handler(message, return_beautiful_picture)
    else:
        bot.send_photo(message.chat.id, caption="Here is your picture! It's so gorgeous!", photo=photo)
        continue_(message)

bot.infinity_polling(none_stop = True)