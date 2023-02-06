from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import json

class SteamAutoJoin():
    def __init__(self, config: dict):
        self.username = config["username"]
        self.password = config["password"]
        self.api_key = config["api_key"]

        self.driver_options = Options()
        self.driver_options.add_experimental_option("detach", True)
        self.driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome("./chromedriver/chromedriver.exe", chrome_options = self.driver_options)

        self.words = [x.lower() for x in json.load(open("./words.txt"))]

    def Start(self):
        print("Starting SteamAutoJoin...")

        print("Logging in...")
        self._login()
        print("Logged in.")

        gid = 1

        while True:
            self._join(gid)
            gid = gid + 1

    def _login(self):
        try:
            self.driver.get("https://steamcommunity.com/login/home/")

            time.sleep(2)

            self.driver.find_elements(By.CLASS_NAME, "newlogindialog_TextInput_2eKVn")[0].send_keys(self.username)
            self.driver.find_elements(By.CLASS_NAME, "newlogindialog_TextInput_2eKVn")[1].send_keys(self.password)
            self.driver.find_element(By.CLASS_NAME, "newlogindialog_SubmitButton_2QgFE").click()

            time.sleep(2)

            if self.driver.find_element(By.CLASS_NAME, "newlogindialog_PrimaryHeader_39uMK").text == "STEAM GUARD":
                self.driver.find_element(By.CLASS_NAME, "newlogindialog_TextLink_1cnUQ").click()

                steam_guard = input("Please enter Steam Guard code: ")

                steam_guard_inputs = self.driver.find_elements(By.XPATH, "//div[@class='newlogindialog_SegmentedCharacterInput_1kJ6q']//input")

                for index, steam_guard_input in enumerate(steam_guard_inputs):
                    steam_guard_input.send_keys(steam_guard[index])

                time.sleep(2)

        except:
            print("Couldn't login, retrying...")
            self._login()

    def _join(self, id: int):
        try:
            self.driver.get(f"https://steamcommunity.com/gid/{id}")

            clantag = self.driver.find_element(By.CLASS_NAME, "grouppage_header_abbrev")

            if not self._check_clantag(clantag.text.lower()):
                return

            self.driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()

            print(f"Joined OG group with id {id}.")

        except:
            pass

    def _check_clantag(self, clantag: str, is_match = re.compile(r"[^a-z0-9]").search) -> bool:
        if (len(clantag) <= 3 and not bool(is_match(clantag))) or clantag in self.words:
            return True

        return False