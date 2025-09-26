import telebot

API_TOKEN = 'ВАШ_ТОКЕН_ТУТ'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот-помощник.")

bot.polling()