# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
import json

from dis import dis
from bangla import convert_english_digit_to_bangla_digit
from datetime import date, datetime
from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import false, true

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher, tracker, domain):
        now = datetime.now()
        am_pm_english = now.strftime("%p")
        am_pm = ""
        if am_pm_english == "AM":
            am_pm = "এএম"
        else:
            am_pm = "পিএম"

        current_time_english = now.strftime("%I:%M:%S")
        current_time = convert_english_digit_to_bangla_digit(current_time_english)
        dispatcher.utter_message(text="এখন সময় হচ্ছে: \t {} {}".format(current_time, am_pm))

        return []

class ActionRainStatus(Action):
    def name(self) -> Text:
        return "action_rain_status"

    def run(self, dispatcher, tracker, domain):
        city_name = tracker.get_slot("city")
        city = getCity(city_name)
        response_json = getWeather(city)
        rain_probability = response_json["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]

        if rain_probability == 1:
            dispatcher.utter_message(text="বৃষ্টি হওয়ার সম্ভাবনা আছে। ছাতা নিয়ে যান।")
        else:
            dispatcher.utter_message(text="বৃষ্টি হওয়ার সম্ভাবনা নেই। ছাতা নিতে হবে না।")

        return []

class ActionWeatherData(Action): 
    def name(self) -> Text:
        return "action_weather_data"
    def run(self, dispatcher, tracker, domain):
        city_name = tracker.get_slot("city")

        city = getCity(city_name)
        json_response = getWeather(city)
        today = json_response['forecast']['forecastday'][0]
        today_day = today['day']
        today_astro = today['astro']
       
        sunrise = convert_english_digit_to_bangla_digit(today_astro["sunrise"])
        sunset = convert_english_digit_to_bangla_digit(today_astro["sunset"])
        max_temp = convert_english_digit_to_bangla_digit(today_day['maxtemp_c'])
        min_temp = convert_english_digit_to_bangla_digit(today_day['mintemp_c'])
        max_wind_speed = convert_english_digit_to_bangla_digit(today_day["maxwind_kph"])
        avg_humidity = convert_english_digit_to_bangla_digit(today_day["avghumidity"])
        rain_chance = convert_english_digit_to_bangla_digit(today_day["daily_chance_of_rain"])
        total_precipitation = convert_english_digit_to_bangla_digit(today_day['totalprecip_mm'])
        weather_condition = convert_english_digit_to_bangla_digit(today_day['condition']['text'])

        get_info_type = tracker.get_slot("weather_info_type")

        if get_info_type == "আবহাওয়া":
            dispatcher.utter_message(text="আজকের আবহাওয়ার সারসংক্ষপ: \n১। সূর্যদোয়: {} \n২। সূর্যাস্ত: {}\n৩। সর্বোচ্চ তাপমাত্রা: {}°C\n৪। সর্বনিম্ন তাপমাত্রা: {}°C\n৫। আর্দ্রতা: {}%\n৬। বৃষ্টি সম্ভাবনা: {}%\n৭। বৃষ্টিপাত: {}mm\n৮। আকাশের অবস্থা: {}\n৯। বাতাসের সর্বোচ্চ গতিবেগ: {}km/h".format(sunrise, sunset, max_temp, min_temp, avg_humidity, rain_chance, total_precipitation, weather_condition, max_wind_speed))
        elif get_info_type == "আকাশের অবস্থা":
            dispatcher.utter_message(text="আজকের আকাশের অবস্থা: {}".format(weather_condition))
        elif get_info_type == "তাপমাত্রা":
            dispatcher.utter_message(text="আজকের তাপমাত্রা: \nসর্বোচ্চ তাপমাত্রা: {}°C\n সর্বনিম্ন তাপমাত্রা: {}°C".format(max_temp, min_temp))   
        elif get_info_type == "বৃষ্টিপাত":
            dispatcher.utter_message(text="আজকের বৃষ্টিপাত: \nআর্দ্রতা: {}%\nবৃষ্টি সম্ভাবনা: {}%\nবৃষ্টিপাত: {}mm".format(avg_humidity, rain_chance, total_precipitation))   
        elif get_info_type == "বায়ুবেগ":
            dispatcher.utter_message(text="আজকের বায়ুবেগ: \nবাতাসের সর্বোচ্চ গতিবেগ: {}km/h".format(sunrise, sunset, max_temp, min_temp, avg_humidity, rain_chance, total_precipitation, weather_condition, max_wind_speed))   
        
        # dispatcher.utter_message(template="utter_weather_info_type")
        return []

class ActionAirQuality(Action):
    def name(self) -> Text:
        return "action_air_quality"

    def run(self, dispatcher, tracker, domain):
        city_name = tracker.get_slot("city")
        aqi_info = getAqi(city_name)
        dispatcher.utter_message(text="বাতাসের মান: {} ({})".format(aqi_info[0], aqi_info[1]))

        return []



def getCity(city_name):
    city = ""   
    if city_name == "রংপুর":
        city = "Rangpur"
    elif city_name == "রাজশাহী":
        city = "Rajshahi"
    elif city_name == "ঢাকা":
        city = "Dhaka"
    elif city_name == "ময়মনসিংহ":
        city = "Mymensingh"
    elif city_name == "সিলেট":
        city = "Sylhet"
    elif city_name == "চট্টগ্রাম":
        city = "Chittagong"
    elif city_name == "বরিশাল":
        city = "Barisal"
    elif city_name == "খুলনা":
        city = "Khulna"
  
    return city


def getWeather(city):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q":city,"days":"3"}
    headers = {
        "X-RapidAPI-Key": "32387ed580msh39b0df6ab10d5edp1f0bc3jsn07d3d5b15939",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_text = response.text
    response_json = json.loads(response_text)
    
    return response_json


def getAqi(city_name):
    lon = 0
    lat = 0
    
    if city_name == "রংপুর":
        lon = 89.2752
        lat = 25.7439
    elif city_name == "রাজশাহী":
        lon = 88.6042
        lat = 24.3745
    elif city_name == "ঢাকা":
        lon = 90.4125
        lat = 23.8103
    elif city_name == "ময়মনসিংহ":
        lon = 90.4203
        lat = 24.7471
    elif city_name == "সিলেট":
        lon = 91.8687
        lat = 24.8949
    elif city_name == "চট্টগ্রাম":
        lon = 91.7832
        lat = 22.3569
    elif city_name == "বরিশাল":
        lon = 90.3535
        lat = 22.7010
    elif city_name == "খুলনা":
        lon = 89.5403
        lat = 22.8456
        
    url = "https://air-quality.p.rapidapi.com/current/airquality"
    querystring = {"lon":lon,"lat":lat}
    headers = {
        "X-RapidAPI-Key": "32387ed580msh39b0df6ab10d5edp1f0bc3jsn07d3d5b15939",
        "X-RapidAPI-Host": "air-quality.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_text = json.loads(response.text)
    
    aqi = response_text["data"][0]["aqi"]
    aqi_status = ""
    if aqi <= 50:
        aqi_status = "ভালো"
    elif aqi > 50 and aqi <= 100:
        aqi_status = "মোটামুটি"
    elif aqi > 100 and aqi <= 150:
        aqi_status = "সংবেদনশীলদের জন্য অস্বাস্থ্যকর"
    elif aqi > 150 and aqi <= 200:
        aqi_status = "অস্বাস্থ্যকর"
    elif aqi > 200 and aqi <= 300:
        aqi_status = "খুবই অস্বাস্থ্যকর"
    elif aqi > 300:
        aqi_status = "মারাত্মক"
        
    aqi = convert_english_digit_to_bangla_digit(aqi) 
    return[aqi, aqi_status]