from selenium import webdriver

class WebDriver():
    def __init__(self):
        self.options: webdriver.ChromeOptions = self.create_options()
        self.driver: webdriver.Chrome = self.create_driver()

    def create_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--window-size= 1920, 1080")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return options

    def create_driver(self) -> webdriver.Chrome:
        return webdriver.Chrome("../chromedriver/chromedriver.exe", chrome_options = self.options)