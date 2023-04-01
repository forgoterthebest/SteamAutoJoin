import SAJ
import os
import colorama
import art

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")

    colorama.init()

    print(art.text2art("SteamAutoJoin")[:-2])
    print(f"By: heapy\nVersion: {SAJ.__version__}\n")

    SAJ.start()