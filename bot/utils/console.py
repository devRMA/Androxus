from colorama import Fore, Style


def log(tag: str, text: str, level: str = 'info', *,
        first_color: str = Fore.CYAN, second_color: str = Fore.LIGHTBLUE_EX):
    print(f'{Style.BRIGHT}{first_color}[{tag:^16}]' +
          f'{second_color}{text}{Style.RESET_ALL}'.rjust(60))
