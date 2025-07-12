import os
import json
import threading
import logging
from api.weather_api import call_weather_api



file_lock = threading.Lock()



def write_data_in_file_json(new_data, filename = "datalog/data.json"):
    try:
        with file_lock:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                        if not(isinstance(data,list)):
                            data = [data]
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

        data.append(new_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(f"Erreur : {e}")
        return False
    



    
def collect_weather_for_city(city, filename):
    try:
        data = call_weather_api(city)
        success = write_data_in_file_json(data, filename=filename)
        if success:
            logging.info(f"✅ Données météo enregistrées pour {city}")
        else:
            logging.warning(f"❌ Échec d'enregistrement pour {city}")
    except Exception as e:
        logging.error(f"⚠️ Erreur pour {city} : {e}")
