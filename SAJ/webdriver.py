from .terminal import Terminal
from selenium import webdriver
from urllib import request
import requests
import os
import zipfile

class WebDriver():
    def __init__(self):
        self.options = self.create_options()
        self.driver = self.create_driver()

    def create_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size= 1920, 1080")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return options

    def create_driver(self) -> webdriver.Chrome:
        self.download_driver()
        return webdriver.Chrome("./SAJ/chromedriver/" + "chromedriver.exe" if os.name == "nt" else "chromedriver", chrome_options = self.options)
    
    def download_driver(self):
        version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text

        if not self.is_latest(version):
            self.remove_chromedriver()

            Terminal.print(f"Downloading ChromeDriver {version}...")

            os.makedirs("./SAJ/chromedriver", exist_ok = True)
            with open("./SAJ/chromedriver/version.txt", "w") as file:
                file.write(version)

            request.urlretrieve(f"https://chromedriver.storage.googleapis.com/{version}/" + "chromedriver_win32.zip" if os.name == "nt" else "chromedriver_linux64.zip", "./SAJ/chromedriver/chromedriver.zip")

            with zipfile.ZipFile("./SAJ/chromedriver/chromedriver.zip", "r") as zip:
                zip.extractall("./SAJ/chromedriver/")

            Terminal.success("Downloaded successfully.")

    def is_latest(self, version) -> bool:
        try:
            with open("./SAJ/chromedriver/version.txt", "r") as file:
                if file.read() == version:
                    return True
            return False
        except:
            return False
        
    def remove_chromedriver(self):
        try:
            os.remove("./SAJ/chromedriver")
        except:
            pass