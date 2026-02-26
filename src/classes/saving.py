## Import all the libraries
import json, os
from functools import reduce
import operator
import classes.singleton as engine

## Savefile class
class Savefile:
    def __init__(self):
        self.save_dir  = engine.game.save_dir                        # Save file directory
        self.savefpath = f"{self.save_dir}/save.json"                # Save file path
        self.base_save = f"{engine.game.project_dir}/base_save.json" # Empty save file path
        self.savefile  = {}
        self.load_data()
    
    def load_data(self):
        try:
            self.savefile = json.loads(open(self.savefpath).read())
        except:
            self.savefile = json.loads(open(self.base_save).read())
    
    def save_data(self):
        try:
            with open(self.savefpath, "w") as f:
                f.write(json.dumps(self.savefile))
        except:
            pass
    
    def get(self, key, fallback=0):
        # Keypath (key/is/here) -> value (self.savefile['key']['is']['here'])
        try:
            return reduce(operator.getitem, key.split('/'), self.savefile)
        except:
            self.set(key, fallback)
            return fallback

    def set(self, key, value):
        # That too, but for set.
        # Return 0 if we chillin, and 1 if this code bit my ass
        try:
            keys = key.split('/')
            d = self.savefile
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = value

            return 0
        except:
            return 1