from .config import Config
from .terminal import Terminal
from .webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import re
import json

class Steam():
    def __init__(self):
        self.config = Config()
        self.driver = WebDriver().driver
        self.words = [x.lower() for x in json.load(open("./SAJ/words.txt"))]

    def start(self):
        Terminal.print("Starting SteamAutoJoin...")
        
        Terminal.print("Logging in...")
        self.login()

        gid = self.config.start_id

        while True:
            self.join(gid)
            gid = gid + 1

    def login(self):
        try:
            login_url = "https://steamcommunity.com/login/home/"
            self.driver.get(login_url)

            time.sleep(2)
            
            login_input = self.driver.find_elements(By.XPATH, "//input[contains(@type, \"text\")]")
            login_input[0].send_keys(self.config.username)
            password_input = self.driver.find_elements(By.XPATH, "//input[contains(@type, \"password\")]")
            password_input[0].send_keys(self.config.password)
            self.driver.find_element(By.XPATH, "//button[contains(@type, \"submit\")]").click()

            time.sleep(2)

            self.check_errors()

            guard_dialog = self.driver.find_elements(By.XPATH, "//div[contains(@class, \"SegmentedCharacterInput\")]") 

            if guard_dialog:
                input = Terminal.input("Enter Steam Guard code: ")
                
                for i, x in enumerate(guard_dialog[0].find_elements(By.XPATH, "//input")):
                    if i > 4:
                        break
                    
                    x.send_keys(input[i])
            else:
                Terminal.print("Waiting until login session will be approved in Steam mobile app.")

            while True:
                current_url = self.driver.current_url
                if current_url != login_url:
                    Terminal.success("Logged in.")
                    break
        except:
            Terminal.error(f"Couldn't login, retrying in 10s...")
            time.sleep(10)
            self.config.set()
            self.login()

    def join(self, id: int):
        try:
            self.driver.get(f"https://steamcommunity.com/gid/{id}")

            clantag = self.driver.find_element(By.CLASS_NAME, "grouppage_header_abbrev")

            if not self.check_clantag(clantag.text.lower()):
                return

            self.driver.find_element(By.CLASS_NAME, "btn_green_white_innerfade").click()

            Terminal.print(f"Joined group with clan tag \"{clantag.text}\" (ID: {id}).")
        except:
            pass

    def check_errors(self):
        error_form = self.driver.find_elements(By.XPATH, "//div[contains(@class, \"FormError\")]")

        if error_form:
            if error_form[0].text != " ":
                raise Exception("Login credentials are not valid")
            
        failure_form = self.driver.find_elements(By.XPATH, "//div[contains(@class, \"Failure\")]")

        if failure_form:
            error_code = self.driver.find_element(By.XPATH, "//div[contains(@class, \"MutedErrorReference\")]")

            raise Exception(f"Failure form appeared with error code: {error_code.text[-3:]}")

    def check_clantag(self, clantag: str, is_match = re.compile(r"[^a-z0-9^.]").search) -> bool:
        if self.config.only_words != "true":
            return True if (len(clantag) <= 3 and not bool(is_match(clantag))) or clantag in self.words else False
        
        return True if clantag in self.words else False
