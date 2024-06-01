BOT_KEY = "5767362118:AAHfunShvYIKvwTeDKuccO6DYmPHi1ekIGM"

## NEA's API

# 5 Minute interval
FIVE_MINUTE_AIR_TEMP_URL = "https://api.data.gov.sg/v1/environment/air-temperature"
FIVE_MINUTE_HUMIDITY_URL = "https://api.data.gov.sg/v1/environment/relative-humidity"
FIVE_MINUTE_WIND_URL = "https://api.data.gov.sg/v1/environment/wind-speed"

FIVE_MINUTE_RAINFALL_URL = "https://api.data.gov.sg/v1/environment/rainfall"

TWOHOURS_FORECAST_URL = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
DAILY_FORECAST_URL = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
FUTURE_FORECAST_URL = "https://api.data.gov.sg/v1/environment/4-day-weather-forecast"

UV_INDEX_URL = "https://api.data.gov.sg/v1/environment/uv-index"
PM25_URL = "https://api.data.gov.sg/v1/environment/pm25"
PSI_URL = "https://api.data.gov.sg/v1/environment/psi"

SINGAPORE_COORDINATES = [1.3521, 103.8198]
WATER_VAPOUR_PRESSURE = 0.33
WIND_SPEED_MULTIPLIER = 0.7
HEAT_INDEX_MULTIPLIER = 4

HI_c1 = -42.379
HI_c2 = 2.04901523
HI_c3 = 10.14333127
HI_c4 = -0.22475541
HI_c5 = -0.00683783
HI_c6 = -0.05481717
HI_c7 = 0.00122874
HI_c8 = 0.00085282
HI_c9 = -0.00000199

DIRECTION_FILTER = ['north', 'south', 'east', 'west', 'all']

WEATHER_EMOJI = {
    'Clear': '☀️',
    'Partly Cloudy': '⛅️',
    'Cloudy': '☁️',
    'Light Rain': '🌧',
    'Thundery Showers': '⛈'
}

TIME_EMOJI = {
    'Afternoon': '🏙',
    'Evening': '🌆',
    'Night': '🌃',
}
## Time examples:
# "Afternoon thundery showers"
# "Late morning and early afternoon thundery showers"

DIRECTION_EMOJI = {
    'N': '⬆️',
    'NNE': '⬆️↗️',
    'NE': '↗️',
    'ENE': '➡️',
    'E': '➡️↗️',
    'ESE': '➡️↘️',
    'SE': '↘️',
    'SSE': '⬇️↘️',
    'S': '⬇️',
    'SSW': '⬇️↙️',
    'SW': '↙️',
    'WSW': '⬅️↙️',
    'W': '⬅️',
    'NNW': '⬆️↖️',
    'NW': '↖️',
    'VARIABLE': '🤷‍♀️'
}