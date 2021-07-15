import render as r
from lib.gamestate import GameState
from render.component import Component
from views import StartPage

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    is_exiting = False

    state = GameState()
    c = r.utils.StateManager({
        "current_page": StartPage,
        "head_component": Component(None)
    })

    while not is_exiting:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            # Start up check.
            r.utils.check_window_size()

            term.clear()
            current_page = c.get_prop("current_page")(state, term, c)
            current_page.render()
            key_press = term.inkey()
            current_page.handle_input(key_press)


if __name__ == "__main__":
    main()
