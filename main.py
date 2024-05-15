import telebot
# import asyncio
import requests

from telebot import types
from config import BOT_KEY, WEATHER_URL
# from telebot.async_telebot import AsyncTeleBot

bot = telebot.TeleBot(BOT_KEY, parse_mode=None)
# bot = AsyncTeleBot(API_KEY)

# Commands
# @bot.message_handler(commands=["hello"])
# def send_greeting(msg):
# 	print("------------------------------")
# 	print(msg)
# 	print("------------------------------")
# 	bot.reply_to(msg, "Howdy, how are you doing?")

# @bot.message_handler(content_types=["photo", "sticker"])
# def send_deny_message(msg):
# 	print("------------------------------")
# 	print(msg)
# 	print("------------------------------")
# 	bot.reply_to(msg, "Bruh thats not a text")

@bot.message_handler(commands=["hello"])
def send_menu(msg):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	
	charlize = types.KeyboardButton('/charlize')
	weather = types.KeyboardButton('/weather')
	dakota = types.KeyboardButton('/dakota')
	quit = types.KeyboardButton('/quit')

	markup.add(charlize, weather, dakota)

	bot.send_message(chat_id=msg.chat.id, text="Hello! What would you like to check out today?", reply_markup=markup)

@bot.message_handler(commands=["charlize"])
def send_greeting(msg):
	print("------------------------------")
	print(msg.chat)
	print("------------------------------")
	bot.reply_to(msg, "Charlize Theron is pretty right god damn")

@bot.message_handler(commands=["weather"])
def send_greeting(msg):
	# bot.reply_to(msg, "Weather is coming soon!")
	markup = types.ReplyKeyboardMarkup(row_width=2)

	twoHour = types.KeyboardButton('/twoHours')

	markup.add(twoHour)

	bot.send_message(chat_id=msg.chat.id, text="What would you like to check?", reply_markup=markup)

@bot.message_handler(commands=['twoHours'])
def two_hour_weather(msg):
	bot.reply_to(msg, "Printing in your console log, please wait!")
	url=WEATHER_URL
	response = requests.get(url)
	print(response.json())

@bot.message_handler(commands=["dakota"])
def send_greeting(msg):
	print("------------------------------")
	print(msg.chat)
	print("------------------------------")
	bot.reply_to(msg, "Fifty Shades of heh")

# @bot.message_handler(commands=["quit"])
# def send_greeting(msg):
# 	print("------------------------------")
# 	print(msg.chat)
# 	print("------------------------------")
# 	bot.reply_to(msg, "Fifty Shades of heh")

# Responses

bot.polling()
# asyncio.run(bot.polling())