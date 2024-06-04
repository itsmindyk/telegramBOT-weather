BOT_KEY = "7473748101:AAFKTY317ObJqxPjNGS6ktyfibfceEF0ttI"

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
# [min_lat, min_lon, max_lat, max_lon]
## taken from wiki
# REGION_AREA = {
#         "C":(1.2486661414312281, 103.76976377059448, 1.352445858568772, 103.87357022940553),
#         "E":(1.2912587832141298, 8.841574987439847, 1.3781852167858701, 8.928525012560153),
#         "N":(1.381370398627283, 0.8994600414311829, 1.485851601372717, 1.0039739585688172),
#         "NE":(1.3457519777267675, 103.84851543029515, 1.4375820222732325, 103.94037256970483),
#         "W":(1.253867985954463, 4.571123078668807, 1.3816880140455368, 4.698976921331193)
# }
## taken from API
# REGION_AREA = {
#         "C": (1.2499549777267676, 103.77407323159181, 1.3417850222732326, 103.86592676840817),
#         "E": (1.3138867832141299, 103.8965245839996, 1.4008132167858702, 103.9834754160004),
#         "N": (1.3657893986272829, 103.7677433951411, 1.470270601372717, 103.87225660485889),
#         "NE": (1.3054601414312281, 103.76809557703486, 1.409239858568772, 103.87190442296513),
#         "W": (1.2934399859544632, 103.63607204775224, 1.421260014045537, 103.76392795224777)
# }
# taken from API + round
REGION_AREA = {
        "C": (1.249955, 103.774073, 1.341785, 103.865927),
        "E": (1.313887, 103.896525, 1.400813, 103.983475),
        "N": (1.365789, 103.767743, 1.470271, 103.872257),
        "NE": (1.305460, 103.768096, 1.409240, 103.871904),
        "W": (1.2934340, 103.636072, 1.421260, 103.763928)
}
## taken from API + round + manual adjust
# REGION_AREA = {
#         "C": (1.249955, 103.774073, 1.341785, 103.865927),
#         "E": (1.313887, 103.896525, 1.400813, 104.5), ##
#         "N": (1.365789, 103.7677, 1.470271, 103.872257),
#         "NE": (1.305460, 103.768096, 1.409240, 103.871904),
#         "W": (1.130488, 103.378457, 1.258308, 103.750) #
# }
## taken from wiki + manual adjustment
# REGION_AREA = {
#         "C": (1.249955, 103.774073, 1.341785, 103.865927),
#         "E": (1.162390, 103.528971, 1.249316, 103.615917), ##
#         "N": (1.365789, 103.767743, 1.470271, 103.872257),
#         "NE": (1.305460, 103.768096, 1.409240, 103.871904),
#         "W": (1.2934340, 103.636072, 1.421260, 103.763928)
# }

KNOTS_TO_KMH = 1.852

HI_c1 = -42.379
HI_c2 = 2.04901523
HI_c3 = 10.14333127
HI_c4 = -0.22475541
HI_c5 = -0.00683783
HI_c6 = -0.05481717
HI_c7 = 0.00122874
HI_c8 = 0.00085282
HI_c9 = -0.00000199

DIRECTION_FILTER = ['north', 'south', 'east', 'west', 'central', 'all']

WEATHER_EMOJI = {
    'Clear': '☀️',
    'Partly Cloudy': '⛅️',
    'Cloudy': '☁️',
    'Light Rain': '🌧',
    'Showers': '🌧',
    'Thundery Showers': '⛈'
}

## Time examples:
# "Afternoon thundery showers"
# "Late morning and early afternoon thundery showers"

## 24 weather descriptions:
# "Moderate rain"

UV_INDEX_LEGEND = {
    ' (Low ✅)': (0, 1, 2),
    ' (Moderate ⚠️)': (3, 4, 5),
    ' (High 🔥)': (6, 7),
    ' (Very High 🔥🔥)': (8, 9, 10),
    ' (Extreme 🔥🔥🔥)': (11, 12, 13)
}

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