import telebot
from telebot import types
from selenium import webdriver

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
current_users = {}
driver = webdriver.Chrome()
driver.get("http://ytroulette.com")


def process_votes():
    return all(value == True for value in current_users.values())


def reset_votes():
    global current_users
    current_users = dict.fromkeys(current_users, False)


def refresh():
    try:
        driver.find_element_by_xpath(
            '/html/body/div[4]/div/div[1]/div[2]/div[1]/div[1]/button').click()
    except Exception as err:
        print(err)


@bot.message_handler(commands=['start', 'admin'])
def send_welcome(message):
    id = message.from_user.id
    current_users[id] = False

    bot.reply_to(message, "Welcome to the Telegra.me bot!")
    markup = types.ReplyKeyboardMarkup(selective=False)
    vote = types.KeyboardButton('VETO')
    exit = types.KeyboardButton('EXIT')
    if message.text == '/admin':
        next = types.KeyboardButton('NEXT')
        markup.row(next)
    markup.row(vote)
    markup.row(exit)
    bot.reply_to(message, "Vote!:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_votes(message):
    voting_user_id = message.from_user.id
    if message.text == 'VETO':
        current_users[voting_user_id] = True
        print(current_users)
        if process_votes():
            bot.send_message(message.chat.id, "SKIPPED")
            refresh()
            reset_votes()
    elif message.text == 'NEXT':
        reset_votes()
        refresh()
    elif message.text == "EXIT":
        current_users.pop(voting_user_id, None)


bot.polling()
