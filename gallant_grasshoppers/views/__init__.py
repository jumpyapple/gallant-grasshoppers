import sys

from blessed import Terminal


class BasePage:
    """Base class for a page."""

    def __init__(self, state: object, term: Terminal, renderstate: dict):
        self.state = state
        self.term = term
        self.renderstate = renderstate

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


sys.path.append("..")


from .game_page import GamePage  # noqa: F401, E402
from .manual_phase import ManualPhasePage  # noqa: F401, E402
from .start_page import StartPage  # noqa: F401, E402
