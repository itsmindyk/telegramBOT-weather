import datetime
import math
import telebot
import requests
from datetime import datetime

from telebot import types
from config import BOT_KEY, WEATHER_URL

# Constants
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)

## Weather
twoHour_URL = WEATHER_URL

## Functions
def getDegrees(lat, lon):

	lat1 = math.radians(1.3521)
	lon1 = math.radians(103.8198)
	lat2 = math.radians(lat)
	lon2 = math.radians(lon)

	# Compute change in coordinates
	delta_lon = lon2 - lon1

	# Compute the bearing
	x = math.sin(delta_lon) * math.cos(lat2)
	y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

	initial_bearing = math.atan2(x, y)

	# Convert the bearing from radians to degrees
	initial_bearing = math.degrees(initial_bearing)

	# Normalize bearings to the range between 0 to 360 degrees
	compass_bearing = (initial_bearing + 360) % 360

	# compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
	compass_brackets = ["N", "S", "E", "W"]

	index = round(compass_bearing / 90) % 4

	return compass_brackets[index]

def addCompassLocation():
	response = requests.get(twoHour_URL)
	area_metadata = response.json()["area_metadata"]

	for place in area_metadata:
		place["compass_direction"] = getDegrees(place["label_location"]["latitude"], place["label_location"]["longitude"])
		place.pop("label_location", None)

	return area_metadata

## UPON STARTUP
area_metadata = addCompassLocation()

# Commands

@bot.message_handler(commands=["hello"])
def send_menu(message):

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

	welcome_greeting = "Weather\n\nLocation: Singapore, Singapore\n\nTemperature: 123\n\nSeason: Tropical\n\n"
	
	twoHours = types.KeyboardButton('/twoHours')
	#twoFourHours = types.KeyboardButton('/24hours')

	markup.add(twoHours)

	bot.send_message(chat_id=message.chat.id, text=welcome_greeting, reply_markup=markup)
	bot.send_message(chat_id=message.chat.id, text="Hello! What would you like to check out today?", reply_markup=markup)

@bot.message_handler(commands=['twoHours'])
def two_hour_forecast(message):

	# Get 2 hours forecast info
	bot.reply_to(message, "Printing in your console log, please wait!")
	response = requests.get(twoHour_URL)
	forecasts = response.json()["items"][0]["forecasts"]
	time_validity = [response.json()["items"][0]["valid_period"]["start"], response.json()["items"][0]["valid_period"]["end"]]

	# Setting the time
	for i, time in enumerate(time_validity):
		dt = datetime.fromisoformat(time)
		local_dt = dt.astimezone()
		time_validity[i] = local_dt.strftime('%I:%M%p').lower()

	bot.send_message(chat_id=message.chat.id, text="Done, please check!")

	twoHours_greeting = "2 Hour Forecast in Singapore: " + time_validity[0] + " to " + time_validity[1] + "\n\n" + "Now Viewing: Central [PLACEHOLDER]"
	
	bot.send_message(chat_id=message.chat.id, text=twoHours_greeting)

	forecast_list = ""

	for place in forecasts:
		forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	bot.send_message(chat_id=message.chat.id, text=forecast_list)

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

	north = types.KeyboardButton('/North')
	south = types.KeyboardButton('/South')
	east = types.KeyboardButton('/East')
	west = types.KeyboardButton('/West')
	all_region = types.KeyboardButton('/AllRegion')

	markup.add(north, south, east, west, all_region)

	bot.send_message(chat_id=message.chat.id, text="Which region would you like to see?", reply_markup=markup)

@bot.message_handler(commands=["North", "South", "East", "West", "AllRegion"])
def send_region_forecast(message):

	bot.send_message(chat_id=message.chat.id, text="You've requested a region, please wait")

	forecast_list = ""
	compass_filter = ""
	region_filter_list = []

	if (message.text == "/North"):
		bot.send_message(chat_id=message.chat.id, text="Its north!")
		compass_filter = "N"

	elif (message.text == "/South"): 
		bot.send_message(chat_id=message.chat.id, text="Its south!")
		compass_filter = "S"

	elif (message.text == "/East"): 
		bot.send_message(chat_id=message.chat.id, text="Its east!")
		compass_filter = "E"

	elif (message.text == "/West"): 
		bot.send_message(chat_id=message.chat.id, text="Its west!")
		compass_filter = "W"
	else:
		bot.send_message(chat_id=message.chat.id, text="No filter, showing the whole of Singapore!")
		compass_filter = ""

	# filter out the selected region from area metadata
	# filter and add the forecast

	if compass_filter != "":
		for area in area_metadata:
			if (area["compass_direction"] == compass_filter):
				region_filter_list.append(area["name"])

	response = requests.get(twoHour_URL)
	forecasts = response.json()["items"][0]["forecasts"]	

	if region_filter_list:
		for place in forecasts:
			if (place["area"] in region_filter_list):
				forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	else: # filter list is empty
		for place in forecasts:
			forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	bot.send_message(chat_id=message.chat.id, text=forecast_list)

## Task 20/5
# 1. do up User-defined constants
# 1a. add emoji to describe the weather (check NEA for the various weather constatns)
# 2. Clean up and simplify the codes
# 3. Add 24 hour forecast
# 3a. Add temperature, humidity (see japanese websites for forecast display ideas)


# Let's get the ball rollin'
bot.polling()


	
