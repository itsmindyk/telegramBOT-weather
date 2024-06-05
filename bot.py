import math
import os
import telebot
import requests
from datetime import datetime

from telebot import types
from telebot.types import Message, CallbackQuery
from config import *
from keep_alive import keep_alive

# Constants
# bot = telebot.TeleBot(BOT_KEY, parse_mode=None)
bot = telebot.TeleBot(token=os.environ.get('token'))

## Functions
def addCompassLocation():
	response = requests.get(TWOHOURS_FORECAST_URL).json()
	area_metadata = response["area_metadata"]

	for place in area_metadata:

		place["compass_direction"] = find_region(place["label_location"]["latitude"], place["label_location"]["longitude"])
		place.pop("label_location", None)

	return area_metadata

def is_within_region(lat, lon, region):

    # Check if a point (lat, lon) is within the bounding box.
    # The bounding box is defined as (min_lat, min_lon, max_lat, max_lon).
    min_lat, min_lon, max_lat, max_lon = region
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

def find_region(lat, lon):

	# Find which bounding box (if any) the point (lat, lon) lies in.
	# Returns the name of the bounding box or None if the point is not in any bounding box.
	for region_name, region_box in REGION_AREA.items():
		# print("hi in for loop, checking the region box: ", region_box)
		# print("hi in for loop, region name: ", region_name)

		if is_within_region(lat, lon, region_box):
			# print("its within region")
			return region_name
		# else:
		# 	return None
		
		# print("going next region to check---------------------------------")

	# return None

def lat_lon_boundary_area(lat, lon, area_sq_km):

    # Approximate conversion factors for latitude and longitude near the equator
    km_per_deg_lat = 111.1  # 1 degree of latitude is approximately 111 km
    # km_per_deg_lon = 111.0 * math.cos(math.radians(lat))  # varies with latitude
    km_per_deg_lon = 111.320 * math.cos(lat)  # varies with latitude


    # Calculate the side length of the bounding box
    side_length_km = math.sqrt(area_sq_km)
    
    # Convert side length to degrees
    delta_lat = side_length_km / km_per_deg_lat
    delta_lon = side_length_km / km_per_deg_lon
    
    # Calculate the bounding box coordinates
    min_lat = lat - delta_lat / 2
    max_lat = lat + delta_lat / 2
    min_lon = lon - delta_lon / 2
    max_lon = lon + delta_lon / 2
    
    return min_lat, min_lon, max_lat, max_lon

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
    
def format_datetime(input_datetime, format):

	dt = datetime.fromisoformat(input_datetime)

	if format == 'datetime':
		# Format the datetime (e.g. 04 june, 2024, 06:00pm)
		formatted = dt.strftime('%d %B, %I:%M%p').lower()

		# To ensure 'am'/'pm' is correctly formatted
		return formatted.replace('am', 'am').replace('pm', 'pm')
	
	elif format == 'time':
		# (e.g. 11:30pm / 11:30am)
		formatted = dt.strftime("%I:%M%p").lower()

		# Convert to desired format (e.g., "11:30pm")
		if formatted[0] == '0':  # Remove leading zero if any
			formatted = formatted[1:]
		return formatted
	
	elif format == 'date':
		# No year (e.g. Friday, 04 June)
		return dt.strftime("%A, %d %B")

	else:
		print('uhhh error in format_datetime')

def get_UV_indicator(value):
	for key, value_range in UV_INDEX_LEGEND.items():
		if value in value_range:
			return key
	return None

############# main features #############
def main_menu(type):
		
	menu = types.InlineKeyboardMarkup()

	# Common Routes
	two = types.InlineKeyboardButton(text="2 Hours Weather", callback_data="two")
	daily = types.InlineKeyboardButton(text="24 Hours", callback_data="daily")
	future = types.InlineKeyboardButton(text="4 Days Ahead", callback_data="future")

	back = types.InlineKeyboardButton(text="Back to Menu", callback_data="menu")

	if type == "main":

		refresh_current = types.InlineKeyboardButton(text="Refresh current weather (every 5 mins)", callback_data="current")
		about = types.InlineKeyboardButton(text="About this Bot", callback_data="about")

		menu.row(refresh_current)
		menu.row(two, daily, future)
		menu.add(about)
	
	elif type == "region":
		north = types.InlineKeyboardButton(text="North", callback_data="north")
		south = types.InlineKeyboardButton(text="Central (South)", callback_data="south")
		east = types.InlineKeyboardButton(text="East", callback_data="east")
		west = types.InlineKeyboardButton(text="West", callback_data="west")
		central = types.InlineKeyboardButton(text="Central (North-East)", callback_data="central")
		all = types.InlineKeyboardButton(text="All Region", callback_data="all")

		menu.row(north, south, east)
		menu.row(west, central, all)
		menu.add(back)

	elif type == "daily":
		menu.row(two, future)
		menu.add(back)

	elif type == "future":
		menu.row(two, daily)
		menu.add(back)

	return menu

def currentForecast(call):

	if isinstance(call, CallbackQuery):
		chat_id = call.message.chat.id
	elif isinstance(call, Message):
		chat_id = call.chat.id

	response = requests.get(FIVE_MINUTE_AIR_TEMP_URL).json()["items"][0]
	response_date_time = response["timestamp"]

	response_air_temp = response["readings"]
	response_humidity = requests.get(FIVE_MINUTE_HUMIDITY_URL).json()["items"][0]["readings"]
	response_wind = requests.get(FIVE_MINUTE_WIND_URL).json()["items"][0]["readings"]

	## Retrieved at 2024-06-02T17:00:00+08:00
	# response_rainfall = requests.get(FIVE_MINUTE_RAINFALL_URL).json()

	response_UV = requests.get(UV_INDEX_URL).json()["items"][0]["index"][0]
	# response_PM25 = requests.get(PM25_URL).json()["items"][0]
	# response_PSI = requests.get(PSI_URL).json()["items"][0]

	# print("response_PM25 API: ", response_PM25)
	# print("response_PSI API: ", response_PSI)

	avgTemp = 0;
	avgHumidity = 0;
	avgWind = 0;

	for temp in response_air_temp:
		temp.pop('station_id')
		avgTemp += temp["value"]
	for humid in response_humidity:
		humid.pop('station_id')
		avgHumidity += humid["value"]
	for wind in response_wind:
		wind.pop('station_id')
		avgWind += wind["value"]

	avgTemp = avgTemp / len(response_air_temp)
	avgHumidity = avgHumidity / len(response_humidity)
	avgWind = (avgWind / len(response_wind)) * KNOTS_TO_KMH
	feels_like_temp = heatIndexCalculator(avgTemp, avgHumidity)

	message = "<u>Temperature now <b>(" + format_datetime(response_date_time, 'datetime') + ")</b></u>\n\n"

	message += "<b>" + str(round(avgTemp)) + "°C</b>\n"
	message += "<i>(Feels like " + str(feels_like_temp) + "°C)</i>\n\n"
	message += 'Average 💧: ' + str(round(avgHumidity)) + '%\n'
	message += 'Average 💨: ' + str(round(avgWind)) + 'km/h\n'
	message += '------------------------------\n' ## 30 lines
	message += 'UV Index (at ' + str(format_datetime(response_UV["timestamp"], 'time')) + '): ' + str(response_UV["value"]) + get_UV_indicator(response_UV["value"]) + '\n'

	bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=chat_id, text="Hello! Which forecast do you want to check out today?", reply_markup=main_menu("main"))

def twoHourForecast(call):

	bot.reply_to(call.message, text="2 hours forecast? Hold on, let me prepare my coconuts...")
	bot.send_message(chat_id=call.message.chat.id, text="Alright, which region do you want to see?", reply_markup=main_menu("region"))

def filterTwoHourForecastByRegion(call):

	reply_msg = "You've requested "+ call.data + ", give me a moment while I filter it!"

	bot.reply_to(call.message, text=reply_msg)

	response = requests.get(TWOHOURS_FORECAST_URL).json()["items"][0]
	forecasts = response["forecasts"]	
	time_validity = response["valid_period"]

	forecast_list = "<u><b>" + call.data.capitalize() + "</b> region, " + str(format_datetime(time_validity["start"], 'time')) + " - " + str(format_datetime(time_validity["end"], 'time')) + "</u>\n\n"
	compass_filter = ""
	region_filter_list = []

	# Setting compass filter
	if (call.data == "north"):
		compass_filter = "N"
	elif (call.data == "south"): 
		compass_filter = "C"
	elif (call.data == "east"): 
		compass_filter = "E"
	elif (call.data == "west"): 
		compass_filter = "W"
	elif (call.data == "central"): 
		compass_filter = "NE"
	else:
		compass_filter = ""

	# Checking if there's a region filtered or not
	if compass_filter != "":
		for area in area_metadata:
			if (area["compass_direction"] == compass_filter):
				region_filter_list.append(area["name"])

	if region_filter_list:
		for place in forecasts:
			if (place["area"] in region_filter_list):
				if len(place["forecast"].split(" ")) > 2:
					place["forecast"] = place["forecast"].split(" ")
					place["forecast"].pop()
					place["forecast"] = ' '.join(place["forecast"])
				forecast_list += "<b>" + place["area"] + ":</b> " + place["forecast"] + " " + WEATHER_EMOJI[place["forecast"]] + "\n"

	else: # filter list is empty
		for place in forecasts:
			if len(place["forecast"].split(" ")) > 2:
				place["forecast"] = place["forecast"].split(" ")
				place["forecast"].pop()
				place["forecast"] = ' '.join(place["forecast"])
			forecast_list += "<b>" + place["area"] + ":</b> " + place["forecast"] + " " + WEATHER_EMOJI[place["forecast"]] + "\n"

	bot.send_message(chat_id=call.message.chat.id, text=forecast_list, parse_mode='HTML')
	bot.send_message(chat_id=call.message.chat.id, text="Which region would you like to see next?", reply_markup=main_menu("region"))

def dailyForecast(call):

	bot.reply_to(call.message, "Daily forecast? Let me hold up my coconuts higher...")
	response = requests.get(DAILY_FORECAST_URL).json()["items"][0]

	time_validity = response["valid_period"]
	weather = response["general"]["forecast"]
	print('weather: ', weather)

	temperature = response["general"]["temperature"]
	avgTemp = sum(temperature.values()) / 2

	humidity = response["general"]["relative_humidity"]
	avgHumidity = sum(humidity.values()) / 2

	wind = response["general"]["wind"]
	avgWind = sum(wind["speed"].values()) / 2

	message = '<u><b>24-Hour forecast</b></u>\n'
	message += 'From ' +str(format_datetime(time_validity["start"], 'datetime')) + '\n\n'

	message += '<b>' + str(round(avgTemp)) + '°C</b> ' + WEATHER_EMOJI[weather] + '\n'
	message += '<i>(Feels like: ' + str(heatIndexCalculator(avgTemp, avgHumidity)) + "°C)</i>\n\n"

	message += '🌡 ' + str(temperature["low"]) + ' ~ ' + str(temperature["high"]) + '°C\n'
	message += '💧 ' + str(round(avgHumidity)) + '%\n'
	message += '💨 ' + str(avgWind) + 'km/h ' + DIRECTION_EMOJI[wind["direction"]] + '\n'
	message += '------------------------------\n' ## 30 lines

	for period in response["periods"]:
		start = period["time"]["start"]
		end = period["time"]["end"]
		if format_datetime(start, 'date') == format_datetime(end, 'date'): ## same day (e.g. Friday, 04 June, 6am - 6pm)
			message += str(format_datetime(start, 'date')) + ", (" + str(format_datetime(start, 'time')) + " - " + str(format_datetime(end, 'time')) + ')\n\n'
		else: ## Different day (04 june, 06:00pm - 05 June, 12am)
			message += str(format_datetime(start, 'datetime')) + " - " + str(format_datetime(end, 'datetime')) + '\n\n'
		for region, weather in period["regions"].items():
			if len(weather.split(" ")) > 2:
				weather = weather.split(" ")
				weather.pop()
				weather = ' '.join(weather)
			message += '<b>' + region.capitalize() + ':</b> ' + weather + ' ' + WEATHER_EMOJI[weather] + '\n'
		message += '------------------------------\n' ## 30 lines

	## menu
	bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=call.message.chat.id, text="Which forecast would you like to check out next?", reply_markup=main_menu("daily"))

def futureForecast(call):
	bot.reply_to(call.message, text="FOUR DAYS?? Wah... let me hold my coconuts higher...")

	response = requests.get(FUTURE_FORECAST_URL).json()["items"][0]
	forecasts = response["forecasts"]

	message = '<b><u>4 Day Outlook</u></b>\n\n'

	for day in forecasts:

		temperature = day["temperature"]
		avgTemp = sum(temperature.values()) / 2

		humidity = day["relative_humidity"]
		avgHumidity = sum(humidity.values()) / 2

		wind = day["wind"]
		avgWind = sum(wind["speed"].values()) / 2

		message += "<b>" + str(format_datetime(day["date"], 'date')) + "</b>\n\n"
		message += '🌡 ' + str(temperature["low"]) + "~" + str(temperature["high"]) + "°C\n"
		message += "<i>(May feel like " + str(heatIndexCalculator(avgTemp, avgHumidity)) + "°C)</i>\n\n"
		message += '💧 ' + str(round(avgHumidity)) + '%\n'
		message += '💨 ' + str(avgWind) + 'km/h ' + DIRECTION_EMOJI[wind["direction"]] + '\n'
		message += '----------------------------------------\n'

	## menu
	bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='HTML')
	bot.send_message(chat_id=call.message.chat.id, text="Which forecast would you like to check out next?", reply_markup=main_menu("future"))

def about_bot_info(call):

	ver_num = 1.0
	note = 'More features coming soon! e.g. Air quality (PSI); Might section out 4 days ahead hmm'
	note += "This is still a fetus, so please don't mind it!"

	message = "<b><u>Version " + str(ver_num) + "</u></b>\n\n"

	message += "Hiya! This is a telegram bot created by Mindy, using NEA's weather data!\n\n"
	
	message += "<b>Creator's Note</b>\n"
	message += note

	bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='HTML', reply_markup=main_menu("region"))

## UPON STARTUP
area_metadata = addCompassLocation()
# print("updated area_metadata: ", area_metadata)

# print('west: ', is_within_region(1.357, 103.987, REGION_AREA["E"]))
# print('west can west or not: ', is_within_region(1.357, 103.987, REGION_AREA["E"]))
# print("west region: ", lat_lon_boundary_area(1.35735, 103.7, 201.3))
# print("west region from wiki: ", lat_lon_boundary_area(1.194398, 103.442381, 201.3))
# print("east region: ", lat_lon_boundary_area(1.35735, 103.94, 93.1))
# print("south (central) region: ", lat_lon_boundary_area(1.35735, 103.82, 132.7))
# print("central (northeast) region: ", lat_lon_boundary_area(1.29587, 103.82, 103.9))
# print("north region: ", lat_lon_boundary_area(1.41803, 103.82, 134.5))

# Commands
@bot.message_handler(commands=["hello", "start"])
def starting_page(message):

	currentForecast(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):

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
	elif call.data == "about":
		about_bot_info(call)

# Let's get the ball rollin'
def main():
    keep_alive()
    bot.polling()

if __name__ == '__main__':
    main()

	
