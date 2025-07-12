import time
import threading
import logging

from storage.file_writer import collect_weather_for_city
from file_parsers.parserjson import JsonParsing





logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
def pipeline_call_weather_api(Json_file = "config/settings.json", compteur_limit_fault:int = 10, file:str = "datalog/datalog.json"):
    """
    compteur_limit_fault: arrêt si le nombre d'erreurs consécutives dépasse cette limite
    
    """
    json_file = JsonParsing()
    json_file.load_json_file()
    cities = json_file.get_attribute_from_json_file("city")
    time_delay = json_file.get_attribute_from_json_file("time_call_api")
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