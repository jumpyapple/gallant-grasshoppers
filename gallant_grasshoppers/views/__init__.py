import sys

from blessed import Terminal

from .start_page import print_start_page  # noqa: F401
from .test_page import print_page2, print_test_page  # noqa: F401

sys.path.append("..")


class BasePage:
    """Base class for a page."""

    def __init__(self, state: object, term: Terminal):
        self.state = state
        self.term = term

    def render(self) -> None:
        """A render method.

        Get called from the main game loop.
        """
        raise NotImplementedError()

    def handle_input(self, key: str) -> None:
        """An input handler.

        Get called from the main game loop.
        """
        raise NotImplementedError()


from .game_page import GamePage  # noqa: F401, E402
from .start_page import StartPage  # noqa: F401, E402
