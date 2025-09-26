import telebot
import random
import requests
API_TOKEN = 'ВАШ_ТОКЕН_ТУТ'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот-помощник.")

@bot.message_handler(commands=['random'])
def send_random(message):
    random_number = random.randint(1, 100)
    bot.reply_to(message, f"Ваше случайное число: {random_number}")
    
@bot.message_handler(commands=['weather'])
def send_weather(message):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=London&appid=ВАШ_API_КЛЮЧ')
    data = response.json()
    weather_description = data['weather'][0]['description']
    bot.reply_to(message, f"Погода в Лондоне: {weather_description}")
    
bot.polling()