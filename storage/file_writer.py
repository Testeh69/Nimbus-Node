import os
import json
import threading




file_lock = threading.Lock()




def write_data_in_file_json(new_data, filename = "datalog/data.json"):
    try:
        with file_lock:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    try:
                        data = [json.load(file)]
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
