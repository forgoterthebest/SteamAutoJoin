import json

class Config():
    def __init__(self):
        self.set()

    def set(self):
        self.username, self.password, self.start_id, self.only_words = self.read()

    def read(self):
        with open("./config.json") as file:
            config = json.load(file)

        return config["username"], config["password"], config["start_id"], config["only_words"]