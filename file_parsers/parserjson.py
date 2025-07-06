import json


class JsonParsing:

    def __init__(self, path = "config/settings.json"):
        self.path = path
        self.data_loaded = None
        self.target_data = None

    def load_json_file(self):
        with open (self.path, encoding="utf-8", mode="r") as file:
            self.data_loaded = json.load(file)
        return self.data_loaded


    def get_attribute_from_json_file(self, attribute:str = "key"):
        self.load_json_file()
        self.target_data = self.data_loaded[attribute]        
        return self.target_data

