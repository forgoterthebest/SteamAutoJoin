from colorama import Fore, Style
from datetime import datetime

class Terminal():
    def print(message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{Terminal.now()}] {message}")

    def input(message: str):
        return input(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{Terminal.now()}] {message}")

    def success(message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{Terminal.now()}] {Fore.GREEN}{message}{Style.RESET_ALL}")

    def error(message: str):
        print(f"[{Fore.BLUE}SAJ{Style.RESET_ALL}] [{Terminal.now()}] {Fore.RED}{message}{Style.RESET_ALL}")

    def now() -> str:
        return datetime.now().strftime("%H:%M:%S")