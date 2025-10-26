from random import choice
from telebot import TeleBot, types
import json

API_TOKEN = '7987526576:AAHUKP7w5kwZG-Pp7tzfLYzxIo6-E2tu2dg'

bot = TeleBot(API_TOKEN)
game = False  # Состояние игры
used_words = []  # Сохраняем здесь все использованные слова
letter = ''  # Буква на которую надо придумать слово



with open('cities.txt', 'r', encoding='utf-8') as f:
    cities = [word.strip().lower() for word in f.readlines()]

def select_letter(text):
    i = -1
    while text[i] in ('ъ', 'ы', 'й', 'ь'):  
        i -= 1
    return text[i]

@bot.message_handler(commands=['goroda'])
def start_game(message):
    global game
    global letter
    game = True
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, text=city)

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    with open('leaders.json', 'r') as f:
        data = json.load(f)
    table = '\n'.join([f"{k},{v}" for k,v in data.values()])
    bot.send_message(message.chat.id, text=table)
    

@bot.message_handler()
def play(message):
    global used_words, letter, game, cities

    if game:
        if message.text.lower() in used_words:
            bot.send_message(message.chat.id,  'Город назывался!')
            return
        elif message.text.lower()[0] != letter:
            bot.send_message(message.chat.id,  'Не та буква!')
            return
        elif message.text.lower() in cities:
            letter = select_letter(message.text.lower())
            used_words.append(message.text.lower())


            add_to_leaderboard(message.from_user)

            #Выбираем город
            choose_cities = []
            for city in cities:
                if city[0] == letter and city not in used_words:
                    choose_cities.append(city)

            # Если бот не смог найти город он проиграл
            if choose_cities == []:
                bot.send_message(message.chat.id, 'Я проиграл')
                game = False

            else:
                city = choice(choose_cities)
                letter = select_letter(city)
                bot.send_message(message.chat.id, city)
                used_words.append(city)

        else: 
            bot.send_message(message.chat.id, 'Такого города не существует!')


# Запускаем бота
bot.polling(none_stop=True)

