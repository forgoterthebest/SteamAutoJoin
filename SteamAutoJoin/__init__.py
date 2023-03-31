from .config import Config
from .steam import Steam
from .webdriver import WebDriver
from .version import version

__version__ = version

def start():
    Steam().start()