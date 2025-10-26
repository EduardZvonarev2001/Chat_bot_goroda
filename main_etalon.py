from random import choice
from telebot import TeleBot, types
import json

API_TOKEN = '!!!!!!!!!!' #ВСТАВЬТЕ ВАШ!!!!!!!

bot = TeleBot(API_TOKEN)
game = False  # Состояние игры
used_words = []  # Сохраняем здесь все использованные слова
letter = ''  # Буква на которую надо придумать слово

leaderboard = {}

with open('cities.txt', 'r', encoding='utf-8') as f:
    cities = [word.strip().lower() for word in f.readlines()]

def select_letter(text):
    i = -1
    while text[i] in ('ъ', 'ы', 'й', 'ь'):  
        i -= 1
    return text[i]

@bot.message_handler(commands=['goroda'])
def start_game(message):
    global game, letter, used_words
    used_words = [] 
    game = True
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, text=city)

@bot.message_handler(commands=['leaderboard'])
def get_leaderboard(message):
    with open('leaders.json', 'r') as f:
        data = json.load(f)
    player_list = [f'{k}: {v}' for k,v in data.items()]
    text = '\n'.join(player_list)
    print(player_list)
    bot.send_message(message.chat.id, text=text)
    

@bot.message_handler(commands=['save'])
def save_leaderboard(message):
    with open('leaders.json', 'w') as f:
        json.dump(leaderboard, f)
    bot.send_message(message.chat.id, text='Успешно сохранено')

@bot.message_handler()
def play(message):
    global used_words, letter, game, cities, leaderboard

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



            if message.from_user.first_name in leaderboard:
                leaderboard[message.from_user.first_name] +=1
            else:
                leaderboard[message.from_user.first_name] = 1

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


