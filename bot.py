import math
import telebot
import requests
from datetime import datetime

from telebot import types
from telebot.types import Message, CallbackQuery
from config import *

# Constants
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)

## Functions
def getDegrees(lat, lon):

	lat1 = math.radians(SINGAPORE_COORDINATES[0])
	lon1 = math.radians(SINGAPORE_COORDINATES[1])
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
	response = requests.get(TWOHOURS_FORECAST_URL).json()
	area_metadata = response["area_metadata"]

	for place in area_metadata:
		place["compass_direction"] = getDegrees(place["label_location"]["latitude"], place["label_location"]["longitude"])
		place.pop("label_location", None)

	return area_metadata

def heatIndexCalculator(avgTemp, avgHumidity):

	## The "feels like" temperature, also known as the apparent temperature, is a measure of how hot or cold it feels to the human body.
	## Heat Index (For Hot Weather) or Wind Chill (For Cold Weather)
	## *Singapore = Heat Index
	
	# "HI" is the Heat Index.
	# "T" is the actual air temperature in degrees Fahrenheit. (F)
	# "RH" is the relative humidity in percentage. (%) 

	## HI = c1 + c2*T +c3*RH +c4*TRH +c5*T2 +c6*RH2 + c7*T2RH + c8*TRH2 + c9*T2RH2
	## Return: calculcated Heat Index temperature in Celcius 

	f_avgTemp = (avgTemp * 9 / 5) +32

	heat_index = HI_c1 + (HI_c2*f_avgTemp) + (HI_c3*avgHumidity) + (HI_c4*avgHumidity*f_avgTemp) + (HI_c5*(f_avgTemp**2)) + (HI_c6*(avgHumidity**2)) + (HI_c7*(f_avgTemp**2)*avgHumidity) + (HI_c8*(avgHumidity**2)*f_avgTemp) + (HI_c9*(avgHumidity**2)*(f_avgTemp**2))
	converted_temp = heat_index - 32
	converted_temp = converted_temp * (5/9)

	return round(converted_temp)	

def format_date(input_str_date):

    # Convert the input string to a datetime object
    date_obj = datetime.strptime(input_str_date, '%Y-%m-%d')
    
    # Get the day of the week and month names
    day_name = date_obj.strftime('%A')  # Full weekday name
    day_number = date_obj.strftime('%d')  # Day of the month
    month_name = date_obj.strftime('%B')  # Full month name
    year = date_obj.strftime('%Y')  # Year
    
    # Add the appropriate suffix to the day number
    if day_number.endswith(('1', '21', '31')):
        suffix = "st"
    elif day_number.endswith(('2', '22')):
        suffix = "nd"
    elif day_number.endswith(('3', '23')):
        suffix = "rd"
    else:
        suffix = "th"
    
    # Construct the formatted string
    return f"{day_name}, {day_number}{suffix}"
    
############# main features #############
def main_menu(type):
		
	menu = types.InlineKeyboardMarkup()

	# Common Routes
	two = types.InlineKeyboardButton(text="2 Hours", callback_data="two")
	daily = types.InlineKeyboardButton(text="24 Hours", callback_data="daily")
	future = types.InlineKeyboardButton(text="4 Days Ahead", callback_data="future")

	back = types.InlineKeyboardButton(text="Back to Menu", callback_data="menu")
	quit = types.InlineKeyboardButton(text="Quit", callback_data="quit")

	if type == "main":

		refresh_current = types.InlineKeyboardButton(text="Refresh current weather", callback_data="current")
		## TO BE ADDED SOON
		about = types.InlineKeyboardButton(text="About this bot", callback_data="about")

		menu.row(refresh_current)
		menu.add(two, daily, future, quit)
	
	elif type == "region":
		north = types.InlineKeyboardButton(text="North", callback_data="north")
		south = types.InlineKeyboardButton(text="South", callback_data="south")
		east = types.InlineKeyboardButton(text="East", callback_data="east")
		west = types.InlineKeyboardButton(text="West", callback_data="west")
		# central = types.InlineKeyboardButton(text="Central", callback_data="central")
		all = types.InlineKeyboardButton(text="All Region", callback_data="all")

		menu.row(north, south, east)
		menu.row(west, all)
		menu.add(back)

	elif type == "daily":
		menu.row(two, future)
		menu.add(back, quit)

	elif type == "future":
		menu.row(two, daily)
		menu.add(back, quit)

	return menu

def currentForecast(call):
	print("I am the  present!")

	if isinstance(call, CallbackQuery):
		print("instance is callback!")
		chat_id = call.message.chat.id
	elif isinstance(call, Message):
		print("instance is callback!")
		chat_id = call.chat.id

	now = datetime.now()
	current_datetime = now.strftime("%m/%d/%Y, %H:%M")
	print("date and time:", current_datetime)

	message = "<u><b>Weather now, " + current_datetime + "</b></u>\n\n"

	response_air_temp = requests.get(FIVE_MINUTE_AIR_TEMP_URL).json()["items"][0]["readings"]
	response_humidity = requests.get(FIVE_MINUTE_HUMIDITY_URL).json()["items"][0]["readings"]
	# response_minute_wind = requests.get(FIVE_MINUTE_WIND_URL).json()["items"][0]

	# response_5minute_rainfall = requests.get(TWOHOURS_FORECAST_URL).json()

	# response_UV = requests.get(TWOHOURS_FORECAST_URL).json()
	# response_PM25 = requests.get(TWOHOURS_FORECAST_URL).json()
	# response_PSI = requests.get(TWOHOURS_FORECAST_URL).json()

	# print("5 min - air temp: ", response_air_temp)
	# print("------------------------------------------------------")
	# print("5 min - HUMDITITY: ", response_humidity)
	# print("------------------------------------------------------")
	# print("5 min - WIND: ", response_minute_wind)
	# print("------------------------------------------------------")

	avgTemp = 0;
	avgHumidity = 0;

	for temp in response_air_temp:
		temp.pop('station_id')
		avgTemp += temp["value"]
	for humid in response_humidity:
		humid.pop('station_id')
		avgHumidity += humid["value"]

	avgTemp = avgTemp / len(response_air_temp)
	avgHumidity = avgHumidity / len(response_humidity)
	feels_like_temp = heatIndexCalculator(avgTemp, avgHumidity)

	message += "<b>" + str(round(avgTemp)) + "°C</b>\n"
	message += "<i>(Feels like " + str(feels_like_temp) + "°C)</i>\n\n"
	message += '💧 ' + str(round(avgHumidity)) + '%\n\n'

	bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=chat_id, text="Hello! Which forecast do you want to check out today?", reply_markup=main_menu("main"))

def twoHourForecast(call):

	bot.reply_to(call.message, text="2 hours forecast? Hold on, let me ask the bomoh!")

	response = requests.get(TWOHOURS_FORECAST_URL).json()
	# print("2 hour api: ", response.json())
	forecasts = response["items"][0]["forecasts"]
	time_validity = [response["items"][0]["valid_period"]["start"], response["items"][0]["valid_period"]["end"]]

	# Setting the time
	for i, time in enumerate(time_validity):
		dt = datetime.fromisoformat(time)
		local_dt = dt.astimezone()
		time_validity[i] = local_dt.strftime('%I:%M%p').lower()

	bot.send_message(chat_id=call.message.chat.id, text="Which region would you like to see?", reply_markup=main_menu("region"))

def filterTwoHourForecastByRegion(call):

	reply_msg = "You've requested "+ call.data + ", give me a moment while I filter it!"

	bot.reply_to(call.message, text=reply_msg)

	forecast_list = ""
	compass_filter = ""
	region_filter_list = []

	# Setting compass filter
	if (call.data == "north"):
		compass_filter = "N"

	elif (call.data == "south"): 
		compass_filter = "S"

	elif (call.data == "east"): 
		compass_filter = "E"

	elif (call.data == "west"): 
		compass_filter = "W"
	else:
		compass_filter = ""

	# Checking if there's a region filtered or not
	if compass_filter != "":
		for area in area_metadata:
			if (area["compass_direction"] == compass_filter):
				region_filter_list.append(area["name"])

	response = requests.get(TWOHOURS_FORECAST_URL).json()
	forecasts = response["items"][0]["forecasts"]	

	if region_filter_list:
		for place in forecasts:
			if (place["area"] in region_filter_list):
				forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	else: # filter list is empty
		for place in forecasts:
			forecast_list += place["area"] + ": " + place["forecast"] + "\n"

	bot.send_message(chat_id=call.message.chat.id, text=forecast_list)
	bot.send_message(chat_id=call.message.chat.id, text="Which region would you like to see next?", reply_markup=main_menu("region"))

def dailyForecast(call):

	bot.reply_to(call.message, "Daily forecast? Let me hold up my two coconuts...")
	response = requests.get(DAILY_FORECAST_URL).json()
	print("response reply: ", response)

	## Set time?

	message = '24-Hour forecast, today:\n\n'

	weather = response["items"][0]["general"]["forecast"]

	temperature = response["items"][0]["general"]["temperature"]
	avgTemp = sum(temperature.values()) / 2

	humidity = response["items"][0]["general"]["relative_humidity"]
	avgHumidity = sum(humidity.values()) / 2

	wind = response["items"][0]["general"]["wind"]
	avgWind = sum(wind["speed"].values()) / 2

	message += '<b>' + str(round(avgTemp)) + '°C</b> ' + WEATHER_EMOJI[weather] + '\n'
	message += '<u>(Feels like: ' + str(heatIndexCalculator(avgTemp, avgHumidity)) + "°C)</u>\n\n"

	message += '🌡 ' + str(temperature["low"]) + ' ~ ' + str(temperature["high"]) + '°C\n\n'

	message += '💧 ' + str(round(avgHumidity)) + '%\n\n'

	message += '💨 ' + str(avgWind) + 'km/h ' + DIRECTION_EMOJI[wind["direction"]] + '\n'

	## menu
	bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=call.message.chat.id, text="Which forecast would you like to check out next?", reply_markup=main_menu("daily"))

def futureForecast(call):
	print("hiya! im 4 days ahead!")
	bot.reply_to(call.message, text="FOUR DAYS?? Wah... let me hold my coconuts higher...")

	response = requests.get(FUTURE_FORECAST_URL).json()
	print("api reply: ", response)
	forecasts = response["items"][0]["forecasts"]
	print("forecasts: ", forecasts)

	# # Setting the time
	# for i, time in enumerate(time_validity):
	# 	dt = datetime.fromisoformat(time)
	# 	local_dt = dt.astimezone()
	# time_validity[i] = local_dt.strftime('%I:%M%p').lower()

	message = '4 Day Outlook:\n----------------------------------------\n'

	# 4 day outlook
	for day in forecasts:
		print("one day: ", day)

		temperature = day["temperature"]
		avgTemp = sum(temperature.values()) / 2

		humidity = day["relative_humidity"]
		avgHumidity = sum(humidity.values()) / 2

		wind = day["wind"]
		avgWind = sum(wind["speed"].values()) / 2

		message += format_date(day["date"]) + ":\n\n"
		time = day["forecast"].split(" ")[0]
		## TODO: get the "thundery showers and map it to emoji in config"
		# weather = day["forecast"].split(" ")
		print("time: ", time)
		# daily_message += TIME_EMOJI[time] + " " + str(temperature["low"]) + "~" + str(temperature["high"]) + "°C\n"
		message += '🌡 ' + str(temperature["low"]) + "~" + str(temperature["high"]) + "°C\n"
		message += "<i>(May feel like " + str(heatIndexCalculator(avgTemp, avgHumidity)) + "°C)</i>\n\n"
		message += '💧 ' + str(round(avgHumidity)) + '%\n\n'
		message += '💨 ' + str(avgWind) + 'km/h ' + DIRECTION_EMOJI[wind["direction"]] + '\n'
		message += '----------------------------------------\n'

	## menu
	bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=call.message.chat.id, text="Which forecast would you like to check out next?", reply_markup=main_menu("future"))

def quit(call):
	print("its time to shutdown!")
	bot.stop_polling()

## UPON STARTUP
area_metadata = addCompassLocation()

# Commands

@bot.message_handler(commands=["hello"])
def starting_page(message):

	currentForecast(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):

	print("in callback, call data: ", call.data)

	if call.data == "two":
		twoHourForecast(call)
	elif call.data in DIRECTION_FILTER:
		filterTwoHourForecastByRegion(call)
	elif call.data == "daily":
		dailyForecast(call)
	elif call.data == "future":
		futureForecast(call)
	elif call.data == "menu" or call.data == "current":
		currentForecast(call)
	elif call.data =="quit":
		quit(call)


#####################################################

## Task 27/5
# 1. put 4 day outlook into a seperate message (too long) [DONE]
# 1a. split the daily forecast into 6 hour intervals???
# 2. tidy up 2 hour forecast section
# 3. work on the current weather info
# 3a. add air quality i.e UV index, PM2.5; add chance of rainfall

# Let's get the ball rollin'
bot.polling()


	
