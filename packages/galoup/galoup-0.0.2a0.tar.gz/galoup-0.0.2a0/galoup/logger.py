import sys

from colorama import Fore, Style, Back

from galoup.error import Error


def normal(line: str, end='\n'):
    print(line, file=sys.stderr, end=end, flush=True)


def bad(line: str):
    print(Fore.RED + line + Style.RESET_ALL, file=sys.stderr, flush=True)


def good(line: str):
    print(Fore.GREEN + Style.BRIGHT + line + Style.RESET_ALL, file=sys.stderr, flush=True)


def error(e: Error):
    print(Style.BRIGHT + Fore.LIGHTWHITE_EX + Back.RED + type(e).__name__ + ":"
          + Style.NORMAL + Back.RESET + Fore.RESET + " " + e.message + Style.RESET_ALL,
          file=sys.stderr, flush=True)


def warning(line: str):
    print(Fore.YELLOW + Style.BRIGHT + line + Style.RESET_ALL, file=sys.stderr, flush=True)
