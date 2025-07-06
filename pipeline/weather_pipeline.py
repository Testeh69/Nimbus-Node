import time
from datetime import datetime
from storage.file_writer import write_data_in_file_json
from api.weather_api import call_weather_api
import logging
import threading
from typing import Union, List
from file_parsers.parserjson import JsonParsing



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


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
def pipeline_call_weather_api(time_delay: int = 1, Json_file = "config/settings.json", compteur_limit_fault:int = 10, file:str = "datalog/datalog.json"):
    """
    time_delay : délai en minutes entre chaque appel API
    city: la ville dont on récupère les données météo
    compteur_limit_fault: arrêt si le nombre d'erreurs consécutives dépasse cette limite
    
    """
    json_file = JsonParsing()
    json_file.load_json_file()
    cities = json_file.get_attribute_from_json_file("city")
    logging.info(f"[INFO] Lancement de la collecte météo pour {cities} toutes les {time_delay} minute(s).")
    continue_call = True
    compteur = 0
    while continue_call:
        try:
            threads = []
            for city in cities:
                filename = f"datalog/{city.lower().replace(',', '_')}.json"
                thread = threading.Thread(target=collect_weather_for_city, args=(city, filename))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            time.sleep(time_delay * 60)
        except KeyboardInterrupt:
            logging.info(f"\n[ 🛑 Arrêt manuel de la collecte.")
            break
        except Exception as e:
            logging.info(f" ⚠️ Erreur inattendue : {e}")
            compteur +=1
            time.sleep(60)

        if compteur >= compteur_limit_fault:
            continue_call = False  