import time
from pathlib import Path

import render as r
from lib.gamestate import GameState, DEFAULT_SAVE_LOCATION, DEFAULT_SAVE_NAME
from render.component import Component
from views import StartPage

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    state = GameState()
    c = r.utils.StateManager({
        "is_exiting": False,
        "current_page": StartPage,
        "head_component": Component(None)
    })

    # Check if there is a save file.
    save_file_path = Path(DEFAULT_SAVE_LOCATION) / DEFAULT_SAVE_NAME
    if save_file_path.exists():
        c.set_prop(("is_save_exist", True))
    else:
        c.set_prop(("is_save_exist", False))

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while not c.get_prop("is_exiting"):
            r.utils.check_window_size()

            current_page = c.get_prop("current_page")(state, term, c)
            current_page.render()

            key_press = term.inkey(timeout=.5)
            time.sleep(1.0/25)  # this helps with screen blinking and gives a smoother experience

            current_page.handle_input(key_press)

    # Saving the game state back to file is handled by the GamePage.


if __name__ == "__main__":
    main()
