

import render as r
from render.component import Component

term = r.terminal()

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

"""
# it needs to be a function for the resizing to work
def print_start_page(sig=None, action=None) -> None:  # type () -> None

    if sig is not None:
        time.sleep(.05)
    print(term.home + term.clear + term.move_y(term.height // 5))
    for i, j in enumerate(boxer_logo):
        term.move_y((term.height // 3)-i)
        print(term.sandybrown(term.center(j)))
    print(term.move_y(int(term.height - 1)))
    print(term.white(term.center("[PRESS SPACE TO CONTINUE]")))
    time.sleep(.05)
"""


def main() -> None:
    """Starts up main function"""
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear + term.move_y(term.height // 2))
            c = Component(None, term.width, term.height, 0, 0, boxer_logo)
            c.draw_component()
            key_press = term.inkey()
        if key_press == " ":
            break


if __name__ == '__main__':
    main()
