from ..config import Config
from ..webdriver import WebDriver
from ..version import version
from selenium.webdriver.common.by import By
import time
import re
import json
import colorama
from colorama import Fore, Style
import art
from datetime import datetime

class Steam():
    def __init__(self):
        self.config = Config()
        self.driver = WebDriver().driver
        self.words = [x.lower() for x in json.load(open("./SteamAutoJoin/words.txt"))]

    def start(self):
        colorama.init()    

        print(art.text2art("SteamAutoJoin")[:-2])
        print(f"by: heapy\nVersion: {version}\n")

        self.print("Starting SteamAutoJoin...")
        self.print("Logging in...")
        self.login()

        gid = self.config.start_id

        while True:
            self.join(gid)
            gid = gid + 1

    def login(self):
        try:
            self.config.read_config()

            login_url = "https://steamcommunity.com/login/home/"
            self.driver.get(login_url)

            time.sleep(2)

            login_inputs = self.driver.find_elements(By.XPATH, "//input[starts-with(@class, \"newlogindialog_TextInput\")]")
            login_inputs[0].send_keys(self.config.username)
            login_inputs[1].send_keys(self.config.password)
            self.driver.find_element(By.XPATH, "//button[starts-with(@class, \"newlogindialog_SubmitButton\")]").click()

            time.sleep(2)

            find_errors = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, \"newlogindialog_FormError\")]")

            if find_errors:
                if find_errors[0].text != " ":
                    raise Exception("Login credentials are not valid")

            steam_guard_dialog = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, \"newlogindialog_SegmentedCharacterInput\")]")

            if steam_guard_dialog:
                input = self.input("Enter Steam Guard code: ")
                
                for i, x in enumerate(steam_guard_dialog[0].find_elements(By.XPATH, "//input")):
                    if i > 4:
                        break
                    
                    x.send_keys(input[i])
            else:
                self.print("If you have Steam Guard enabled, accept login session from your mobile Steam app.")

            while True:
                current_url = self.driver.current_url
                if current_url != login_url:
                    self.success("Logged in.")
                    break
        except Exception as e:
            self.error(f"Couldn't login, retrying in 10s... {e}")
            time.sleep(10)
            self.login()

    def join(self, id: int):
        try:
            self.driver.get(f"https://steamcommunity.com/gid/{id}")

            clantag = self.driver.find_element(By.CLASS_NAME, "grouppage_header_abbrev")

            if not self._check_clantag(clantag.text.lower()):
                return

            self.driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()

            self.print(f"Joined group with clan tag \"{clantag.text}\" (ID: {id}).")
        except:
            pass

    def _check_clantag(self, clantag: str, is_match = re.compile(r"[^a-z0-9^.]").search) -> bool:
        if self.config.only_words != "true":
            return True if (len(clantag) <= 3 and not bool(is_match(clantag))) or clantag in self.words else False
        
        return True if clantag in self.words else False

    def print(self, message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{self._now()}] {message}")

    def input(self, message: str):
        return input(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{self._now()}] {message}")

    def success(self, message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{self._now()}] {Fore.GREEN}{message}{Style.RESET_ALL}")

    def error(self, message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{self._now()}] {Fore.RED}{message}{Style.RESET_ALL}")

    def _now(self) -> str:
        return datetime.now().strftime("%H:%M:%S")