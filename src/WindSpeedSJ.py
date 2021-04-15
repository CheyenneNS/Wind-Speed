# WindSpeedSJ.py file

"""
Usage:
WindSpeedSJ.py  --minutes <int> [--metric <bool>]
WindSpeedSJ.py  --minutes <int> [--imperial <bool>]
WindSpeedSJ.py  --hours <int> [--metric <bool>]
WindSpeedSJ.py  --hours <int> [--imperial <bool>]

Required options:
  --minutes <int>
  --hours <int>

Options:
   --metric=<bool>
   --imperial=<bool>  default: True
"""

# Imports
from docopt import docopt
import sys
import schedule
import time
import datetime

# Function imports
from unittest import TestCase
from WindSpeedImpl import WindData
from WindSpeedImpl import check_windspeed


def main():
   """
   main of WindSpeedSJ: initiates a WindObj and calls scheduler.
   """
   args = docopt(__doc__)
   windObj = WindData()
   scheduler(args, windObj)

def scheduler(args, windObj):
   """
   Schedules run events for check_windspeed function based on input params; args.
   Input: args from user, windObj to hold wind information
   """
   if args['--minutes']:
      minutes = int(args['--minutes'])
   elif args['--hours']:
      minutes = 60*int(args['--hour'])

   if args['--metric']:
      check_windspeed(windObj, 'metric')
      schedule.every(1).minutes.do(check_windspeed, 'metric', windObj)
   else:
      check_windspeed(windObj)
      schedule.every(1).minutes.do(check_windspeed, windObj)
   schedule.every(minutes).minutes.do(exit)

   while True:
      schedule.run_pending()
      time.sleep(1)


def exit():
   print('{} Wind Speed program will now exit '.format(datetime.datetime.now()))  # this works
   sys.exit()


if __name__ == '__main__':
   main()
