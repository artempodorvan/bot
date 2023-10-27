import telebot
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
import time
import random
import os
import database as db
from database import log_in, users
import location as loc

url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
url1 = 'https://coinmarketcap.com/currencies/bitcoin/'
url2 = 'https://deepstatemap.live/en'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

TOKEN = '6436836130:AAHhM-eGRz8rGtjIPkJN4y1hZ7eKX8qrDU8'
bot = telebot.TeleBot(TOKEN)

user_dates = {}
waiting_for_image = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hi boss, I\'m Kesha. How can I help you?')
    bot.send_message(message.chat.id, 'U can have two types of functions user and admin to have admin func u need'
                                      ' to pay on card 4149 5001 1106 7289 Raiffeisen BANK and send a picture'
                                      ' on my number +38 068 889 5045 then i\'ll give u a command.'
                                      ' To have func write "/help"')

@bot.message_handler(commands=['help'])
def help_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton('U help me support Ukraine',
                                              url='https://bank.gov.ua/ua/about/support-the-armed-forces')
    markup.row(btn1)
    btn2 = telebot.types.InlineKeyboardButton('Destroyed tanks from russia',
                                              callback_data='info_machine')
    btn3 = telebot.types.InlineKeyboardButton('Image customer', callback_data='ch_image')
    markup.row(btn2, btn3)

    btn4 = telebot.types.InlineKeyboardButton('Bitcoin graph', callback_data='Screen')
    btn5 = telebot.types.InlineKeyboardButton('Sticker from Kesha', callback_data='sticker')
    btn6 = telebot.types.InlineKeyboardButton('Map of Ukraine', callback_data='map')
    markup.row(btn4, btn5, btn6)
    btn7 = telebot.types.InlineKeyboardButton('Delete previous message', callback_data='delete')
    markup.row(btn7)
    btn8 = telebot.types.InlineKeyboardButton('Sign up database', callback_data='sign_up')
    btn9 = telebot.types.InlineKeyboardButton('Log in database', callback_data='log_in')
    markup.row(btn8, btn9)

    bot.send_message(message.chat.id, 'Hi boss, I\'m Kesha. How can I help you?', reply_markup=markup)

@bot.message_handler(commands=['special_key-Forrr_AdMIiN-_telegram:artem\'s_topgKeSHaa'])
def special_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn9 = telebot.types.InlineKeyboardButton('List of users in database', callback_data='list_users')
    btn10 = telebot.types.InlineKeyboardButton('Delete user', callback_data='delete_user')
    markup.row(btn9)
    markup.row(btn10)
    btn6 = telebot.types.InlineKeyboardButton('Get Screenshot', callback_data='get_screenshot')
    markup.row(btn6)

    bot.send_message(message.chat.id, 'Hi ADMIN, I\'m Kesha. And these are secret functions which belong only to you', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    chat_id = callback.message.chat.id
    data = callback.data

    if data == 'info_machine':
        bot.send_message(chat_id, 'Please enter a date in the format DD.MM.YYYY (e.g., 20.04.2023)')
        user_dates[chat_id] = True
    elif data == 'ch_image':
        bot.send_message(chat_id, 'Please send the image you want to convert to black and white.')
        waiting_for_image[chat_id] = True
    elif data == 'Screen':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url1)
        driver.save_screenshot("screenshot.png")
        driver.quit()
        with open('screenshot.png', 'rb') as f:
            bot.send_photo(chat_id, f)
    elif data == 'map':
        driver = webdriver.Chrome()
        driver.get(url2)
        time.sleep(7)
        driver.save_screenshot("screenshot1.png")
        driver.quit()
        with open('screenshot1.png', 'rb') as f:
            bot.send_photo(chat_id, f)
    elif data == 'delete':
        amount_deleting = 10
        i = 1
        try:
            while i <= amount_deleting:
                bot.delete_message(chat_id, callback.message.message_id - i)
                i += 1
        except Exception as e:
            bot.send_message(chat_id, f'Failed to delete the messages: {e}')
    elif data == 'sticker':
        chat_id1 = callback.message.chat.id
        s = random.randint(0, 5)
        if s == 1:
            file_id = 'CAACAgIAAxkBAAIrY2Uz7bKecLZe5_rVKymas50DNagtAALeAAP0exkAAb2F7273xc49MAQ'
            bot.send_sticker(chat_id1, file_id)
        elif s == 2:
            file_id = 'CAACAgIAAxkBAAIrZmUz7cHDvd62YmmLcyc4oSK5tA4bAAIDAQACVp29CgLl0XiH5fpPMAQ'
            bot.send_sticker(chat_id1, file_id)
        elif s == 3:
            file_id = 'CAACAgIAAxkBAAIraWUz7cgpS4OSnyd-XoSav59OfKk_AAL_AANWnb0K2q36feS8QCQwBA'
            bot.send_sticker(chat_id1, file_id)
        elif s == 4:
            file_id = 'CAACAgIAAxkBAAIrbGUz7c6sc5rCn81nZgmqBxIpaJ - CAAL - AANWnb0K2gRhMC751_8wBA'
            bot.send_sticker(chat_id1, file_id)



    elif data == 'sign_up':
        bot.send_message(chat_id, 'Enter your name in chat')
        bot.register_next_step_handler(callback.message, sign_up_name)  # this function can keep your sms in chat

    elif data == 'log_in':
        bot.send_message(chat_id, 'Enter your name in chat')
        bot.register_next_step_handler(callback.message, log_in_name)

    elif data == 'list_users':
        db.users()
        admin_users = users()
        users_text = "\n".join(admin_users)
        bot.send_message(chat_id, users_text)

    elif data == 'delete_user':
        bot.send_message(chat_id, 'Enter the username you want to delete')
        bot.register_next_step_handler(callback.message, delete_user_username)

    elif data == 'get_screenshot':
        send_all_images(chat_id)

# below u have functions to use in a future from database upstairs u can see
def sign_up_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, 'Enter your password in chat')
    bot.register_next_step_handler(message, sign_up_password, name=name)


def sign_up_password(message, name):
    chat_id = message.chat.id
    password = message.text
    db.sign_up(name, password)
    admin_result1 = log_in(name, password)
    if admin_result1 == 'U passed':
        bot.send_message(chat_id, 'Hi admin, you have passed. Below you have special functions')
    elif admin_result1 == 'U did not':
        bot.send_message(chat_id,
                         'You registered successfully. Unfortunately,'
                         ' you are NOT an admin, and you have functions only for users')

        loc.content(name)

    elif admin_result1 == 'U did not find any users':
        bot.send_message(chat_id, 'In this database, there are no users')



def log_in_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, 'Enter your password in chat')
    bot.register_next_step_handler(message, log_in_password, name=name)

def log_in_password(message, name):
    chat_id = message.chat.id
    password = message.text
    admin_result = log_in(name, password)
    if admin_result == 'U passed':
        bot.send_message(chat_id, 'Hi admin, you have passed. Below you have special functions')
        bot.send_message(chat_id, "Enter this line inside quotes '/special_key-Forrr_"
              "AdMIiN-_telegram:artem's_topgKeSHaa'"
              " in your chat to have admin functions")
    elif admin_result == 'U did not':
        bot.send_message(chat_id, 'Unfortunately, you are NOT an admin, and you have functions only for users')
    elif admin_result == 'U did not find any users':
        bot.send_message(chat_id, 'In this database, there are no users')

def delete_user_username(message):
    chat_id = message.chat.id
    username = message.text
    bot.send_message(chat_id, 'Enter the password of the user you want to delete')
    bot.register_next_step_handler(message, delete_user_password, username=username)

def delete_user_password(message, username):
    chat_id = message.chat.id
    password = message.text

    db.delete_user(username, password)

def send_all_images(chat_id):
    folder_name = 'images'

    if os.path.exists(folder_name):
        image_files = [f for f in os.listdir(folder_name) if f.endswith('.png')]

        if image_files:
            for image_file in image_files:
                image_path = os.path.join(folder_name, image_file)
                with open(image_path, 'rb') as f:
                    bot.send_photo(chat_id, f, caption=image_file)
        else:
            bot.send_message(chat_id, 'In folder doesn\'t exist anything')
    else:
        bot.send_message(chat_id, 'The folder doesn\'t exist')

@bot.message_handler(func=lambda message: True)
def handle_date_input(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id in user_dates and user_dates[chat_id]:
        user_dates[chat_id] = False

        elements = soup.find_all('li', class_='gold')
        found = False

        for element in elements:
            day = element.find('span')
            if day:
                day_numbers = day.text.strip()
                if day_numbers == text:
                    found = True
                    element_div = element.find_next('div', class_='casualties')
                    if element_div:
                        element_text = element_div.text.strip()
                        if element_text:
                            bot.send_message(chat_id, f'Statistics of crushed machines by ЗСУ {day_numbers}')
                            bot.send_message(chat_id, element_text)
                            break

        if not found:
            bot.send_message(chat_id, 'No information found for the entered date.')

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    chat_id = message.chat.id
    if chat_id in waiting_for_image and waiting_for_image[chat_id]:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(TOKEN, file_info.file_path))

        with open('input_image.jpg', 'wb') as f:
            f.write(file.content)

        img = Image.open('input_image.jpg')
        baw = img.convert('L')
        baw.save('output_image.jpg')

        with open('output_image.jpg', 'rb') as f:
            bot.send_photo(chat_id, f)

        waiting_for_image[chat_id] = False

bot.polling(none_stop=True)
