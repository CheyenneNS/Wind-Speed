# WindSpeedSJ.py file
'''
Usage:
WindSpeedSJ.py [options]

unit-option:
   --metric=<bool>
   --imperial=<bool>  [default: True]


'''

from docopt import docopt
import requests
import sys
import schedule
import time
import datetime

def main():

   args = docopt(__doc__)
   print(args)
   global velocity
   velocity = float('-inf')
   scheduler(args)

#class WindData(object):
   #def __init__(self, velocity):
      #self.velocity = velocity


def wind_direction(degreesFromNorth):
   compass = {
      range(349, 11): 'N',
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
      range(326, 349): 'NNW'}

   for k, v in compass.items():
      if degreesFromNorth in k:
         return v


def exit():
   print('{} Now the system will exit '.format(datetime.datetime.now()))  # this works
   sys.exit()

def check_windspeed(unit="imperial"):

   response = requests.get(
         "https://api.openweathermap.org/data/2.5/weather?q=san+jose&appid=3207703ee5d0d14e6b6a53d10071018f&units=" + unit)
   wind_data = response.json()['wind']
   wind_speed = float(wind_data['speed'])
   global velocity

   if velocity != wind_speed:
      velocity = wind_speed
      degrees = int(wind_data['deg'])
      units = {"imperial": "mi/h", "metric": "m/s"}
      direction = wind_direction(degrees)
      result = str(wind_data['speed']) + " " + units[unit] + " " + direction
      print(result)


def scheduler(args):

   if args['--metric']:
      check_windspeed('metric')
      schedule.every(1).minutes.do(check_windspeed, 'metric')
   else:
      check_windspeed()
      schedule.every(1).minutes.do(check_windspeed)
   schedule.every(3).minutes.do(exit)

   while True:
      schedule.run_pending()
      time.sleep(1)

if __name__ == '__main__':
   main()
