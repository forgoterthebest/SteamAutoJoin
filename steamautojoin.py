from steamwebapi.api import ISteamUser
from steam.webapi import WebAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class SteamAutoJoin():
    def __init__(self, config: dict):
        self.username = config["username"]
        self.password = config["password"]
        self.api_key = config["api_key"]

        self.userclient = ISteamUser(steam_api_key = self.api_key)
        self.webclient = WebAPI(key = self.api_key)
        # self.groups = self.userclient.get_user_group_list(ENTER_YOUR_STEAMID64_HERE)

        self.driver_options = Options()
        self.driver_options.add_experimental_option("detach", True)
        self.driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome("./chromedriver/chromedriver.exe", chrome_options = self.driver_options)

    def Start(self):
        print("Starting SteamAutoJoin...")

        print("Logging in...")
        self.Login()
        print("Logged in.")

        gid = 1

        while True:
            self.Join(gid)
            gid = gid + 1

    def Login(self):
        try:
            self.driver.get("https://steamcommunity.com/login/home/")

            time.sleep(2)

            self.driver.find_elements(By.CLASS_NAME, "newlogindialog_TextInput_2eKVn")[0].send_keys(self.username)
            self.driver.find_elements(By.CLASS_NAME, "newlogindialog_TextInput_2eKVn")[1].send_keys(self.password)
            self.driver.find_element(By.CLASS_NAME, "newlogindialog_SubmitButton_2QgFE").click()

            time.sleep(1)

            if self.driver.find_element(By.CLASS_NAME, "newlogindialog_PrimaryHeader_39uMK").text == "STEAM GUARD":
                self.driver.find_element(By.CLASS_NAME, "newlogindialog_TextLink_1cnUQ").click()

                steam_guard = input("Please enter Steam Guard code: ")

                steam_guard_inputs = self.driver.find_elements(By.XPATH, "//div[@class='newlogindialog_SegmentedCharacterInput_1kJ6q']//input")

                for index, steam_guard_input in enumerate(steam_guard_inputs):
                    steam_guard_input.send_keys(steam_guard[index])

                time.sleep(2)
        except:
            print("Couldn't login, retrying...")

    def Join(self, id: int):
        try:
            # if id in self.groups["response"]["groups"]:
            #     print(f"Already joined group {id}.")
            #     return

            self.driver.get(f"https://steamcommunity.com/gid/{id}")
            self.driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()

            time.sleep(0.5)

        except:
            print(f"Couldn't join group with id {id}.")