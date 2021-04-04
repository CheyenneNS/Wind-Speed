# Imports
import requests


class WindData(object):
   """
   The wind data object contains wind velocity information.

   Attributes
   ----------
   speed : float
   degrees : float
           Stores degree of wind from due north
   direction: str
            Stores return str of direction from wind degree
   """

   def __init__(self):
      self.speed = float('-inf')
      self.degrees = float('inf')
      self.direction = None


def call_api(url):
   """
   Function call_api queries Open Weather API for wind data in San Jose

   """
   try:
      response = requests.get(url)
      if not response:
         raise Exception("Invalid API key. Please check url is valid.")
   except requests.exceptions.ConnectionError as errc:
      print("Error Connecting:", errc)
      raise SystemExit(errc)

   except requests.exceptions.Timeout as errt:
      print("Timeout Error:", errt)
      raise SystemExit(errt)

   wind_data = response.json()['wind']
   return wind_data


def check_windspeed(windObj, unit="imperial"):
   """
   Queries Open Weather Map API for wind data in San Jose Ca.
   Places data from query into a wind object and prints information to terminal.
   """

   units = {"imperial": "mi/h", "metric": "m/s"}
   url = "https://api.openweathermap.org/data/2.5/weather?q=san+jose&appid=3207703ee5d0d14e6b6a53d10071018f&units=" \
         + unit

   wind_data = call_api(url)
   wind_speed = float(wind_data['speed'])
   windspeed_prev = windObj.speed

   if windspeed_prev != wind_speed:
      windObj.speed = wind_speed

      degrees = int(wind_data['deg'])
      windObj.degrees = degrees
      direction = wind_direction(degrees)
      windObj.direction = direction
      resultInfo = 'Current wind speed in San Jose: {} {} {}'.format(wind_data['speed'], units[unit], direction)
      print(resultInfo)
      return resultInfo


def wind_direction(degreesFromNorth):
   """
   Categorizes the wind direction from degree information
   >>> wind_direction(30)
   'NNE'
   >>> wind_direction(257)
   'WSW'
   >>> wind_direction(1000)
   ValueError: Degree input of 1000 out of range.
   """
   compass = {
      range(351, 11): 'N',
      range(11, 34): 'NNE',
      range(34, 56): 'NE',
      range(56, 79): 'ENE',
      range(79, 101): 'E',
      range(101, 124): 'ESE',
      range(124, 146): 'SE',
      range(146, 169): 'SSE',
      range(169, 191): 'S',
      range(191, 214): 'SSW',
      range(214, 236): 'SW',
      range(236, 259): 'WSW',
      range(259, 281): 'W',
      range(281, 304): 'WNW',
      range(304, 326): 'NW',
      range(326, 351): 'NNW'}

   for k, v in compass.items():
      if degreesFromNorth in k:
         return v
   raise ValueError('Degree input of {} out of range.'.format(degreesFromNorth))
