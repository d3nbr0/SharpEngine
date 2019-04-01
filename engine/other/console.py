from colorama import Fore, Style


def log(text):
    print('[SharpEngine] {}'.format(text))


def process(text):
    log(Fore.YELLOW + text + Style.RESET_ALL)


def success(text):
    log(Fore.GREEN + text + Style.RESET_ALL)


def error(text):
    log(Fore.RED + text + Style.RESET_ALL)
