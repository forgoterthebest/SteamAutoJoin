import json

class Config():
    def __init__(self, config_path = "./config.json"):
        self.config_path = config_path
        self.username, self.password, self.start_id, self.only_words = self.read_config()

    def read_config(self):
        config_file = open(self.config_path)
        config = json.load(config_file)
        config_file.close()

        return config["username"], config["password"], config["start_id"], config["only_words"]