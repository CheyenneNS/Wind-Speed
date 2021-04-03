import unittest
from unittest.mock import patch
from WindSpeed.src.WindSpeedSJ import check_windspeed
from WindSpeed.src.WindSpeedSJ import WindData
from WindSpeed.src.WindSpeedSJ import wind_direction
from WindSpeed.src.WindSpeedSJ import call_api
import requests
import mock


class CheckWindSpeedTest(unittest.TestCase):

    def testWindInformation(self):
        # test for correct wind data in meters
        wind_data = WindData()
        unit = "metric"
        units = {"imperial": "mi/h", "metric": "m/s"}

        response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=san+jose&appid=3207703ee5d0d14e6b6a53d10071018f&units=" + unit)
        wind_info = response.json()['wind']
        wind_speed = float(wind_info['speed'])
        degrees = int(wind_info['deg'])

        direction = wind_direction(degrees)
        wind_data.degrees = degrees
        wind_data.velocity = wind_speed
        wind_data.direction = direction

        result_test1 = 'Current wind speed in San Jose: {} {} {}'.format(wind_data.velocity,
                                                                         units[unit],
                                                                         wind_data.direction)
        self.assertEqual(check_windspeed(WindData(), unit), result_test1)

        wind_data.velocity = 1000
        result_test2 = 'Current wind speed in San Jose: {} {} {}'.format(wind_data.velocity,
                                                                         units[unit],
                                                                         wind_data.direction)
        self.assertNotEqual(check_windspeed(WindData()), result_test2)

    def _mock_response(self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses, so its usually a good idea
        to have a helper function that builds these things

        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('WindSpeedSJ.requests.get')  # Mock 'requests' module 'get' method.
    def test_failed_api_call(self, mock_get):
        mock_resp = self._mock_response(status=401)
        mock_get.return_value.status_code = mock_resp
        url = "https://api.openweathermap.org/data/2.5/weat"
        self.assertRaises(Exception, call_api, url, msg='Invalid API key. Please check url is valid.')


if __name__ == '__main__':
    unittest.main()

