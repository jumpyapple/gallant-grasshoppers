from pathlib import Path

import render as r
from blessed import Terminal
from lib.gamestate import DEFAULT_SAVE_LOCATION, DEFAULT_SAVE_NAME, GameState
from render.component import Component, PopupMessage
from views import StartPage

DEBUG = True
term = r.terminal()


def should_get_currency_achievement(achievement: dict, state: GameState) -> bool:
    """Abstraction of the checking for currency achievement."""
    return state.getCash() >= achievement["CONDITION"]["amount"]


def should_get_generator_archievement(achievement: dict, state: GameState) -> bool:
    """Abstraction of the checking for generator achievement."""
    generator_id = achievement["CONDITION"]["generator_id"]
    generators = state.getGenerators()

    if generator_id not in generators.keys():
        return False
    return generators[generator_id]["amount"] >= achievement["CONDITION"]["amount"]


def achievement_checking(
    term: Terminal, state: GameState, render_state: r.utils.StateManager
) -> None:
    """Check achievement and display a popup."""
    for achievement in state.earnable_achievements:
        if achievement["CONDITION"]["type"] == "CURRENCY":
            if should_get_currency_achievement(achievement, state):
                popup = PopupMessage(
                    term, render_state, achievement["DISPLAY_TEXT"], y=4
                )
                render_state.set_prop(("current_popup", popup))

                # Mark achievement as earned.
                state.earnAchievement(achievement["ID"])
        elif achievement["CONDITION"]["type"] == "GENERATOR":
            if should_get_generator_archievement(achievement, state):
                popup = PopupMessage(
                    term, render_state, achievement["DISPLAY_TEXT"], y=4
                )
                render_state.set_prop(("current_popup", popup))

                # Mark achievement as earned.
                state.earnAchievement(achievement["ID"])


def main() -> None:
    """Starts up main function"""
    state = GameState()
    c = r.utils.StateManager(
        {
            "is_exiting": False,
            "is_in_game": False,
            "current_page": StartPage,
            "current_popup": None,
            "head_component": Component(None),
            "current_menu": state.available_generators
        }
    )

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
                # start = time.time()
                current_page.render()
                # end = time.time()
                # print(end - start)
                # If there is any popup, we are rendering it on top
                # of everything else.
                popup = c.get_prop("current_popup")
                if popup:
                    popup.render()

                key_press = term.inkey(timeout=.5)

                # TODO: jumpyapple - Add a trap for ESC key.
                # This may have to be in each page since ESC may be used to dismiss
                # sub-menu/dialog/etc.

                # If there is a popup, it will receive the input first.
                if popup and not popup.auto_dismiss:
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
