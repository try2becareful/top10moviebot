import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("API")

names = {'Боевики': 'boeviki', 'Приключения': 'adventures', 'Детективы': 'detective', 'Для детей': 'detskiy',
         'Драмы': 'drama', 'Зарубежные': 'foreign', 'Исторические': 'istoricheskie', 'Комедии': 'comedy',
         'Триллеры': 'thriller', 'Ужасы': 'horror', 'Фантастика': 'fantastika', 'Фэнтази': 'fentezi',
         'Спорт': 'sport', 'Мелодрамы': 'melodramy', 'Документальные': 'documentary', 'Биография': 'biography'}


keyboard = telebot.types.ReplyKeyboardMarkup(True)  # Клавиатура
keyboard.row('Боевики', 'Приключения')
keyboard.row('Детективы', 'Для детей')
keyboard.row('Драмы', 'Зарубежные')
keyboard.row('Исторические', 'Комедии')
keyboard.row('Триллеры', 'Ужасы')
keyboard.row('Фантастика', 'Фэнтази')
keyboard.row('Спорт', 'Мелодрамы')
keyboard.row('Документальные', 'Биография')


cat = ['Боевики', 'Приключения', 'Детективы', 'Для детей', 'Драмы', 'Зарубежные', 'Исторические', 'Комедии', 'Триллеры',
       'Ужасы', 'Фантастика', 'Фэнтази', 'Спорт', 'Мелодрамы', 'Документальные', 'Биография']
'''
to_href = ['boeviki', 'adventures', 'detective', 'detskiy', 'drama', 'foreign', 'istoricheskie', 'comedy', 'thriller',
           'horror', 'fantastika', 'fentezi', 'sport', 'melodramy', 'documentary', 'biography']
'''

href1 = 'https://www.ivi.ru/movies/'
href2 = '?paid_type=avod'


@bot.message_handler(commands=['start'])  # Команда /start
def start(msg):
    bot.send_message(msg.chat.id,
                     "Привет, постараюсь помочь тебе с выбором. Узнай список команд с помощью /help")


@bot.message_handler(commands=['categories'])  # Команда /categories
def categories(msg):
    message = bot.send_message(msg.chat.id, "Выберете жанр", reply_markup=keyboard)
    bot.register_next_step_handler(message, ans)


@bot.message_handler(commands=['help'])  # Команда /help
def help(msg):
    bot.send_message(msg.chat.id, "/start - начало работы ")
    bot.send_message(msg.chat.id, "/categories - выбор жанра")


@bot.message_handler(content_types=['text'])  # Воспринимание текста
def text(msg):  # Случай непонятного сообщения
    if msg not in cat:
        bot.send_message(msg.chat.id, "Выберете команду, список команд /help")


def ans(msg):  # Выбор жанра
    if msg.text not in cat:
        bot.send_message(msg.chat.id, "Выберете команду, список команд /help")
    else:
        url = href1 + names.get(msg.text) + href2
        bot.send_message(msg.chat.id, url)
        responce = requests.get(url).text
        soup = BeautifulSoup(responce, "lxml")
        movie_name = soup.find_all("div", class_="nbl-slimPosterBlock__title")  # Название фильма
        movie_info = soup.find_all("div", class_="nbl-poster__propertiesRow")  # Информация о фильме
        movie_rating = soup.find_all("div", class_="nbl-ratingCompact__valueInteger")  # Рейтинг фильма
        for i in range(10):
            bot.send_message(msg.chat.id, movie_name[i])
            bot.send_message(msg.chat.id, movie_info[i])
            bot.send_message(msg.chat.id, movie_rating[i])
            bot.send_message(msg.chat.id, "---------------------")


bot.polling(none_stop=True)
