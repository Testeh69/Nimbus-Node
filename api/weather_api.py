from file_parsers.parserjson import JsonParsing
from datetime import datetime
import requests



def call_weather_api(city = "Evreux,Fr"):
    Json_file = JsonParsing()
    key = Json_file.get_attribute_from_json_file()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    response = requests.get(url)
    data = response.json()
    data["timestamp"] = datetime.now().isoformat()

    return data