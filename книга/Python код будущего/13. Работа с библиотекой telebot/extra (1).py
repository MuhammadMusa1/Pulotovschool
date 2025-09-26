import telebot
import random

API_TOKEN = 'ВАШ_ТОКЕН_ТУТ'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот-помощник.")

@bot.message_handler(commands=['random'])
def send_random(message):
    random_number = random.randint(1, 100)
    bot.reply_to(message, f"Ваше случайное число: {random_number}")
    
bot.polling()