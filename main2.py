import telebot

bot = telebot.TeleBot("5767362118:AAEWa1eZXg4XL7kEyh3qHByFGNmGwXbEg1M", parse_mode=None)

@bot.message_handler(commands=["start"])
def send_welcome(msg):
    bot.reply_to(msg, "wtf you want")

@bot.message_handler(func=lambda message:True)
def echo_all(msg):
    bot.reply_to(msg, msg.text)

bot.infinity_polling()