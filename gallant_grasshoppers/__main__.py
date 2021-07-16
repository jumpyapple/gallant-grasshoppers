import time
from pathlib import Path

import render as r
from lib.gamestate import GameState, DEFAULT_SAVE_LOCATION, DEFAULT_SAVE_NAME
from render.component import Component, PopupMessage
from views import StartPage

DEBUG = True
term = r.terminal()

is_achievement_received = False

def achievement_checking(term, state, render_state):
    # TODO: jumpyapple - Moving this to GameState?
    global is_achievement_received
    if state.getCash() > 0 and state.getCash() <= 1 and not is_achievement_received:
        is_achievement_received = True
        popup = PopupMessage(term, render_state, "Your first box!", y=4)
        render_state.set_prop(("current_popup", popup))

def main() -> None:
    """Starts up main function"""
    state = GameState()
    c = r.utils.StateManager({
        "is_exiting": False,
        "is_in_game": False,
        "current_page": StartPage,
        "current_popup": None,
        "head_component": Component(None)
    })

    # Check if there is a save file.
    save_file_path = Path(DEFAULT_SAVE_LOCATION) / DEFAULT_SAVE_NAME
    if save_file_path.exists():
        c.set_prop(("is_save_exist", True))
    else:
        c.set_prop(("is_save_exist", False))

    try:

        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            while not c.get_prop("is_exiting"):
                r.utils.check_window_size()

                if c.get_prop("is_in_game"):
                    achievement_checking(term, state, c)

                current_page = c.get_prop("current_page")(state, term, c)
                current_page.render()

                # If there is any popup, we are rendering it on top
                # of everything else.
                popup = c.get_prop("current_popup")
                if popup:
                    popup.render()

                key_press = term.inkey(timeout=.5)
                time.sleep(1.0/25)  # this helps with screen blinking and gives a smoother experience

                # TODO: jumpyapple - Add a trap for ESC key.
                # This may have to be in each page since ESC may be used to dismiss
                # sub menu.

                # If there is a popup, it will receive the input first.
                if popup:
                    popup.handle_input(key_press)
                else:
                    current_page.handle_input(key_press)
    except Exception as e:
        if DEBUG:
            raise e
        else:
            with term.cbreak():
                print(term.home + term.clear)
                popup = PopupMessage(term, c, f"Unexpected error D: [{str(e)}]")
                popup.render()
                term.inkey()
    # Saving the game state back to file is handled by the GamePage.


if __name__ == "__main__":
    main()
