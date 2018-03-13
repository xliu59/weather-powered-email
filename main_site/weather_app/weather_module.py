from urllib import request
import datetime
import json
from .models import Subscriber


# param dictionary for api
params = {
    "current_api": "http://api.wunderground.com/api/%s/conditions/q/%s/%s.json", # fill (key_id, state_abbr, city_name)
    "history_api": "http://api.wunderground.com/api/%s/history_%s/q/%s/%s.json", # (key_id, date, state_abbr, city_name)
    "key_id": "ed2193adacdd7605",  # Wundergroud weather api development api key
}


def get_weather(state, city):
    """
    Request to api's to get the weather info, including :
        weather  : weather condition, e.g. 'Cloudy'
        temp     : current temperature in Fahrenheit, e.g. 51.6
        mean_temp: mean temperature in Fahrenheit of last year same day, e.g. 49.3
    :param state : string state abbreviation, e.g. 'NY'
    :param city  : string city name, e.g. 'New York'
    :return      : dictionary {"state": str, "city": str, "weather": str, "temp": float, "mean_temp": float}
    """

    api_params = ('%s', state, city.replace(' ', '_'))    # assemble api-required params, use "New_York" not "New York"
    curr_weather = get_data_from_api('current_api', api_params)      # request the current weather api
    weather = curr_weather['current_observation']['weather']         # according to the api-returned json format
    temp = curr_weather['current_observation']['temp_f']             # according to the api-returned json format

    last_year = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime("%Y%m%d")
    api_params = ('%s', last_year, state, city.replace(' ', '_'))
    hist_weather = get_data_from_api('history_api', api_params)      # request the history weather api
    mean_temp = float(hist_weather['history']['dailysummary'][0]['meantempi'])

    return {"state": state, "city": city, "weather": weather, "temp": temp, "mean_temp": mean_temp}


def get_data_from_api(api_type, api_param):
    """
    Requst specific api with given params, return response

    :param api_type : string, key of chosen api in param dictionary
    :param api_param: tuple, values to be filled into api url
    :return:  api-returned json data
    """
    url = params[api_type] % api_param % params["key_id"]
    with request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data
