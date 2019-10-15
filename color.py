from colorama import Fore, Back, Style


def error(msg):
    colored(msg, fore=Fore.RED)


def warning(msg):
    colored(msg, fore=Fore.LIGHTRED_EX)


def info(msg):
    colored(msg, fore=Fore.GREEN)


def debug(msg):
    colored(msg, fore=Fore.CYAN)


def colored(msg, fore=Fore.RESET, back=Back.RESET):
    print("{}{}{}".format(fore, back, msg))
