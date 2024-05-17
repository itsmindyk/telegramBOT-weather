import math
import telebot
# import asyncio
import requests

from telebot import types
from config import BOT_KEY, WEATHER_URL
# from telebot.async_telebot import AsyncTeleBot

# Constants
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)

## Weather
twoHourURL = WEATHER_URL
singaporeLatLon = [1.3521, 103.8198]

## Functions

def locationMetadata ():
	print("in locationMetadata")

def getDegrees(lat, lon):
	print("in getDegrees")

	lat1 = math.radians(singaporeLatLon[0])
	lon1 = math.radians(singaporeLatLon[1])
	lat2 = math.radians(lat)
	lon2 = math.radians(lon)

	# Compute change in coordinates
	delta_lon = lon2 - lon

	# Compute the bearing
	x = math.sin(delta_lon) * math.cos(lat)
	y = math.cos(lat1) * math.sin(lat) - (math.sin(lat1) * math.cos(lat) * math.cos(delta_lon))

	initial_bearing = math.atan2(x, y)

	# Convert the bearing from radians to degrees
	initial_bearing = math.degrees(initial_bearing)

	# Normalize bearings to the range between 0 to 360 degrees
	compass_bearing = (initial_bearing + 360) % 360

	compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

	index = round(compass_bearing / 45) % 8

	return compass_brackets[index]


# Commands

# @bot.message_handler(content_types=["photo", "sticker"])
# def send_deny_message(msg):
# 	print("------------------------------")
# 	print(msg)
# 	print("------------------------------")
# 	bot.reply_to(msg, "Bruh thats not a text")

@bot.message_handler(commands=["hello"])
def send_menu(message):

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	
	charlize = types.KeyboardButton('/charlize')
	weather = types.KeyboardButton('/weather')

	markup.add(charlize, weather)

	bot.send_message(chat_id=message.chat.id, text="Hello! What would you like to check out today?", reply_markup=markup)

@bot.message_handler(commands=["charlize"])
def send_greeting(message):
	print("------------------------------")
	print(message.chat)
	print("------------------------------")
	bot.reply_to(message, "Charlize Theron is pretty right god damn")

@bot.message_handler(commands=["weather"])
def send_greeting(message):

	# Get Location info
	response = requests.get(twoHourURL)
	area_metadata = response.json()["area_metadata"]

	for place in area_metadata:
		print("place: ", place)
		place["label_location"]["compass_direction"] = getDegrees(place["label_location"]["latitude"], place["label_location"]["longitude"])

	print("finished adding all compass: ", area_metadata)

	# Menu: Asking types of forecast
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

	twoHour = types.KeyboardButton('/twoHours')

	markup.add(twoHour)

	## 1. give user the current location's weather
	weather_greeting = "Weather\n\nLocation: Singapore, Singapore\n\nTemperature: 123\n\nSeason: Tropical\n\n"

	bot.send_message(chat_id=message.chat.id, text=weather_greeting)
	bot.send_message(chat_id=message.chat.id, text="What would you like to check?", reply_markup=markup)

@bot.message_handler(commands=['twoHours'])
def two_hour_forecast(message):
	bot.reply_to(message, "Printing in your console log, please wait!")
	response = requests.get(twoHourURL)
	# print(response.json())
	forecasts = response.json()["items"][0]["forecasts"]
	print("forecasts: ", forecasts)
	bot.send_message(chat_id=message.chat.id, text="Done, please check!")

	# Types of weather:
	# Sunny, partly cloudy, showers, thundery showers

	twoHours_greeting = "2 Hour Forecast in Singapore\n\n 2pm to 4pm\n\n Now Viewing: Central [PLACEHOLDER]"
	
	bot.send_message(chat_id=message.chat.id, text=twoHours_greeting)

	forecast_list = ""

	for place in forecasts:
		forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	bot.send_message(chat_id=message.chat.id, text=forecast_list)

	# # Serangoon
	# print("from getDegrees, compass bearing: ", getDegrees(1.357, 103.865))

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

	twoHour = types.KeyboardButton('/West')
	twoHour = types.KeyboardButton('/North')
	twoHour = types.KeyboardButton('/South')
	twoHour = types.KeyboardButton('/East')

	bot.send_message(chat_id=message.chat.id, text="Which area would you like to see?", reply_markup=markup)

	# Tasks
	
	## 2. narrow down to 4 broad directions
	## 3. filter by specific weather

# Responses

bot.polling()


	
