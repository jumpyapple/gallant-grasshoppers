
from blessed import Terminal

from . import BasePage

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
    "'----------------'  '----------------'  '----------------'  '----------------'  '----------------'",
]


class StartPage(BasePage):
    """
    The start page of the game.

    :param state: The game state.
    :param term: The terminal object from blessed.
    """

    def __init__(self, state: object, term: Terminal):
        super().__init__(state, term)

    def render(self) -> None:
        """Creates start page, can be called from signal module and directly"""
        print(
            self.term.home + self.term.clear + self.term.move_y(self.term.height // 5)
        )
        for i, j in enumerate(boxer_logo):
            self.term.move_y((self.term.height // 3) - i)
            print(self.term.sandybrown(self.term.center(j)))
        print(self.term.move_y(int(self.term.height - 1)))
        print(self.term.white(self.term.center("[PRESS SPACE TO CONTINUE]")))

    def handle_input(self, key: str) -> None:
        """Handler for an input."""
        return None
