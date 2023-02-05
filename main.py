from steamautojoin import SteamAutoJoin
import json
import os

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    config_file = open("./config.json")
    config = json.load(config_file)
    config_file.close()

    SteamAutoJoin(config).Start()