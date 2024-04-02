import json
import os

class Store:
    _instance = None 

    _data = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Store, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            if os.path.isfile('data.json'):
                with open('data.json', 'r') as f:
                    self._data = json.load(f)
        except:
            pass

    def set_value(self, key, value):
        self._data[key] = value
        with open('data.json', 'w') as f:
            json.dump(self._data, f)

    def get_value(self, key):
        if key in self._data:
            return self._data[key]
        else:
            return None
