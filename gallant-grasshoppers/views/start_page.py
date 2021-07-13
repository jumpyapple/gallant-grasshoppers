
from blessed import Terminal
from render import Component  # ignore this. it is correct syntax

boxer_logo = [
    " .----------------.  .----------------.  .----------------.  .----------------.  .----------------.",
    "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |",
    "| |   ______     | || |     ____     | || |  ____  ____  | || |  _________   | || |  _______     | |",
    "| |  |_   _ \\    | || |   .'    `.   | || | |_  _||_  _| | || | |_   ___  |  | || | |_   __ \\    | |",
    "| |    | |_) |   | || |  /  .--.  \\  | || |   \\ \\  / /   | || |   | |_  \\_|  | || |   | |__) |   | |",
    "| |    |  __'.   | || |  | |    | |  | || |    > `' <    | || |   |  _|  _   | || |   |  __ /    | |",
    "| |   _| |__) |  | || |  \\  `--'  /  | || |  _/ /'`\\ \\_  | || |  _| |___/ |  | || |  _| |  \\ \\_  | |",
    "| |  |_______/   | || |   `.____.'   | || | |____||____| | || | |_________|  | || | |____| |___| | |",
    "| |              | || |              | || |              | || |              | || |              | |",
    "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |",
    " '----------------'  '----------------'  '----------------'  '----------------'  '----------------'"
]


# issue with this logo, centers styles should fix once made


def print_start_page() -> None:
    """Creates start page, can be called from signal module and directly"""
    term = Terminal()
    c = Component(None, term.width // 2 - len(boxer_logo[0]) // 2,
                  term.height // 3 - len(boxer_logo) // 2, data=boxer_logo)
    # c.set_styles(["border"])
    c.draw_component()
    print(term.move_y(int(term.height - 1)))
    print(term.white(term.center("[PRESS SPACE TO CONTINUE]")))
