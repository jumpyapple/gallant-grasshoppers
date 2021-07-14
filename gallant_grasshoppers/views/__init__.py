class BasePage:
    """Base class for a page."""

    def __init__(self, state, term):
        self.state = state
        self.term = term

    def render(self):
        raise NotImplementedError()

    def handle_input(self, key):
        raise NotImplementedError()


from .start_page import StartPage  # noqa: F401
from .game_page import GamePage
