import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import json
import colorama
from colorama import Fore, Back, Style
import art

class SteamAutoJoin():
    def __init__(self, config: dict):
        self.username = config["username"]
        self.password = config["password"]
        self.start_id = config["start_id"]
        self.only_words = config["only_words"]

        self.driver_options = Options()
        self.driver_options.headless = True
        self.driver_options.add_argument("--window-size= 1920, 1080")
        self.driver_options.add_experimental_option("detach", True)
        self.driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = selenium.webdriver.Chrome("./chromedriver/chromedriver.exe", chrome_options = self.driver_options)

        self.words = [x.lower() for x in json.load(open("./words.txt"))]
        self.version = "1.0.1"

    def Start(self):
        colorama.init()    

        print(art.text2art("SteamAutoJoin")[:-2])
        print(f"by: heapy\nVersion: {self.version}\n")

        self._print("Starting SteamAutoJoin...")
        self._print("Logging in...")
        self._login()

        gid = self.start_id

        while True:
            self._join(gid)
            gid = gid + 1

    def _login(self):
        try:
            login_url = "https://steamcommunity.com/login/home/"
            self.driver.get(login_url)

            time.sleep(2)

            login_inputs = self.driver.find_elements(By.XPATH, "//input[starts-with(@class, \"newlogindialog_TextInput\")]")
            login_inputs[0].send_keys(self.username)
            login_inputs[1].send_keys(self.password)
            self.driver.find_element(By.XPATH, "//button[starts-with(@class, \"newlogindialog_SubmitButton\")]").click()

            time.sleep(2)

            find_errors = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, \"newlogindialog_FormError\")]")

            if find_errors:
                if find_errors[0].text != " ":
                    raise Exception("Login credentials are not valid")

            self._print("If you have Steam Guard enabled, accept login session from your mobile Steam app. (Reworked version of entering Steam Guard code soon).")

            while True:
                current_url = self.driver.current_url
                if current_url != login_url:
                    self._success("Logged in.")
                    break

        except:
            self._error("Couldn't login, retrying in 10s...")
            time.sleep(10)
            self._login()

    def _join(self, id: int):
        try:
            self.driver.get(f"https://steamcommunity.com/gid/{id}")

            clantag = self.driver.find_element(By.CLASS_NAME, "grouppage_header_abbrev")

            if not self._check_clantag(clantag.text.lower()):
                return

            self.driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()

            self._print(f"Joined group with clan tag \"{clantag.text}\" (ID: {id}).")

        except:
            pass

    def _check_clantag(self, clantag: str, is_match = re.compile(r"[^a-z0-9^.]").search) -> bool:
        if self.only_words != "true":
            if (len(clantag) <= 3 and not bool(is_match(clantag))) or clantag in self.words:
                return True

        else:
            if clantag in self.words:
                return True

        return False

    def _print(self, message: str):
        print(f"[ {Fore.BLUE}SAJ{Style.RESET_ALL} ] {message}")

    def _success(self, message: str):
        print(f"[ {Fore.BLUE}SAJ{Style.RESET_ALL} ] {Fore.GREEN}{message}{Style.RESET_ALL}")

    def _error(self, message: str):
        print(f"[ {Fore.BLUE}SAJ{Style.RESET_ALL} ] {Fore.RED}{message}{Style.RESET_ALL}")