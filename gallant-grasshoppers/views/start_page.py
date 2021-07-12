import time

from ..render import get_term as terminal

boxer_logo = [
    ".----------------.  .----------------.  .----------------.  .----------------.  .----------------.",
    "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |",
    "| |   ______     | || |     ____     | || |  ____  ____  | || |  _________   | || |  _______     | |",
    "| |  |_   _ \\    | || |   .'    `.   | || | |_  _||_  _| | || | |_   ___  |  | || | |_   __ \\    | |",
    "| |    | |_) |   | || |  /  .--.  \\  | || |   \\ \\  / /   | || |   | |_  \\_|  | || |   | |__) |   | |",
    "| |    |  __'.   | || |  | |    | |  | || |    > `' <    | || |   |  _|  _   | || |   |  __ /    | |",
    "| |   _| |__) |  | || |  \\  `--'  /  | || |  _/ /'`\\ \\_  | || |  _| |___/ |  | || |  _| |  \\ \\_  | |",
    "| |  |_______/   | || |   `.____.'   | || | |____||____| | || | |_________|  | || | |____| |___| | |",
    "| |              | || |              | || |              | || |              | || |              | |",
    "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |",
    "'----------------'  '----------------'  '----------------'  '----------------'  '----------------'"
]


def print_start_page(sig: int = None) -> None:
    """Creates start page, can be called from signal module and directly"""
    if sig is not None:
        time.sleep(.05)
    term = terminal()
    print(term.home + term.clear + term.move_y(term.height // 5))
    for i, j in enumerate(boxer_logo):
        term.move_y((term.height // 3)-i)
        print(term.sandybrown(term.center(j)))
    print(term.move_y(int(term.height - 1)))
    print(term.white(term.center("[PRESS SPACE TO CONTINUE]")))
    time.sleep(.05)
