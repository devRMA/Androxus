from colorama import Fore, Style


def log(tag, text, first_color=Fore.CYAN, second_color=Fore.LIGHTBLUE_EX):
    print(f'{Style.BRIGHT}{first_color}[{tag:^16}]' +
          f'{second_color}{text}{Style.RESET_ALL}'.rjust(60))
