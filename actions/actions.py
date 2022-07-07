# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
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
        is_raining = False

        if is_raining:
            dispatcher.utter_message(text="বৃষ্টি হওয়ার সম্ভাবনা আছে। ছাতা নিয়ে যান।")
        else:
            dispatcher.utter_message(text="বৃষ্টি হওয়ার সম্ভাবনা নেই। ছাতা নিতে হবে না।")

        return []

class ActionWeatherData(Action): 
    def name(self) -> Text:
        return "action_weather_data"
    def run(self, dispatcher, tracker, domain):
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        city = tracker.get_slot("city")
        querystring = {"q":city,"days":"3"}

        return []