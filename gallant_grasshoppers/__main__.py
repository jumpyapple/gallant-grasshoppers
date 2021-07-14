# from render.component import Component

from . import render as r
from .lib.gamestate import GameState
from .views import GamePage, StartPage

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    key_press = ""
    is_exiting = False

    state = GameState()
    current_page = StartPage(state, term)

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # Start up check.
        r.utils.check_window_size()

        while not is_exiting:
            current_page.render()

            key_press = term.inkey(timeout=0.5)
            current_page.handle_input(key_press)

            # TODO: "There must be a better way"
            if key_press == "q":
                if isinstance(current_page, StartPage):
                    is_exiting = True
                elif isinstance(current_page, GamePage):
                    current_page = StartPage(state, term)
            elif key_press == " ":
                if isinstance(current_page, StartPage):
                    current_page = GamePage(state, term)


if __name__ == "__main__":
    main()
