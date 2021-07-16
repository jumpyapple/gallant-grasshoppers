import json

import render as r  # ignore this. it is correct syntax
from blessed import Terminal

from . import BasePage
from .game_page import GamePage
from .manual_phase import ManualPhasePage

Component = r.Component
boxer_logo = [
    " .----------------.  .----------------.  .----------------.  .----------------.  .----------------.",
    "| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |",
    "| |   ______     | || |     ____     | || |  ____  ____  | || |  _________   | || |  _______     | |",
    "| |  |_   _ \\    | || |   .'    `.   | || | |_  _||_  _| | || | |_   ___  |  | || | |_   __ \\    | |",
    "| |    | |_) |   | || |  /  .--.  \\  | || |   \\ \\  / /   | || |   | |_  \\_|  | || |   | |__) |   | |",
    "| |    |  __'.   | || |  | |    | |  | || |    > `' <    | || |   |  _|  _   | || |   |  __ /    | |",
    "| |   _| |__) |  | || |  \\  `--'  /  | || |  _/ /'`\\ \\_  | || |  _| |___/ |  | || |  _| |  \\ \\_  | |",
    "| |  |_______/   | || |   `.____.'   | || | |____||____| | || | |_________|  | || | |____| |___| | |",
    "| |              | || |              | || |              | || |              | || |              | |",
    "| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |",
    " '----------------'  '----------------'  '----------------'  '----------------'  '----------------'",
]


class StartPage(BasePage):
    """
    The start page of the game.

    :param state: The game state.
    :param term: The terminal object from blessed.
    """

    def __init__(self, state: object, term: Terminal, renderstate: object):
        super().__init__(state, term, renderstate)
        self.comps = []
        self.current_cursor = None

    def render(self) -> None:
        """Creates start page, can be called from signal module and directly"""
        main = self.renderstate.get_prop("head_component")
        c = Component(main, self.term.width // 2 - len(boxer_logo[1]) // 2,
                      self.term.height // 3, children=boxer_logo, selectable=False)
        c.set_wh(5, 5)
        c2 = Component(main, self.term.width // 2, self.term.height - 1, ["Exit"], selectable=True, id="exit")
        c2.set_wh(1, 1)
        c3 = Component(main, self.term.width // 2, self.term.height - 7, ["New session"], selectable=True, id="next")
        c3.set_wh(1, 1)
        c2.set_callback(self.exit_handler)
        c3.set_callback(self.new_game_handler)

        credit_btn = Component(main, self.term.width // 2, self.term.height - 4, ["Credit"], selectable=True, id="credit")
        credit_btn.set_wh(1, 1)
        credit_btn.set_callback(self.credit_handler)

        # Add a "continue" button if there is a save file.
        is_save_exist = self.renderstate.get_prop("is_save_exist")
        if is_save_exist:
            continue_btn = Component(main, self.term.width // 2, self.term.height - 10, ["Continue"], selectable=True, id="continue")
            continue_btn.set_wh(1, 1)
            continue_btn.set_callback(self.continue_handler)
            main.set_children([c, continue_btn, c3, credit_btn, c2])
        else:
            main.set_children([c, c3, credit_btn, c2])

        children = main.get_children()
        self.comps = []
        for i in children:
            if isinstance(i, Component) and i.is_selectable():
                self.comps.append(i)

        self.current_cursor = self.comps[0]

        for i in self.comps:
            try:
                if self.renderstate.get_prop("cursor").get_id() == i.get_id():
                    self.current_cursor = i
                    break
            except AttributeError:
                break

        self.current_cursor.set_styles({"border": True})
        main.draw_component()

    def handle_input(self, key: any) -> None:
        """Handler for an input."""
        if key == " ":
            self.current_cursor.select()
        if key == "q":
            exit(0)
        elif key and key.is_sequence:
            if key.name == "KEY_DOWN":
                self.current_cursor = self.comps[(self.comps.index(self.current_cursor) + 1) % len(self.comps)]
                self.renderstate.set_prop(("cursor", self.current_cursor))
            elif key.name == "KEY_UP":
                self.current_cursor = self.comps[self.comps.index(self.current_cursor) - 1]
                self.renderstate.set_prop(("cursor", self.current_cursor))

    def new_game_handler(self):
        # jumypapple: Now, we are loading the data.
        # TODO: jumpyapple - ask for confirmation if a save is already exist.
        self.state.state = self.state.newGame()
        self.renderstate.set_prop(("current_phase", "manual"))
        self.renderstate.set_prop(("current_page", ManualPhasePage))
        self.renderstate.set_prop(("is_in_game", True))

    def continue_handler(self):
        self.state.state = self.state.loadGame(None, None)

        # Determine which phase to load into.
        self.state.phase = self.state.state["phase"]
        self.renderstate.set_prop(("current_phase", self.state.phase))
        self.renderstate.set_prop(("is_in_game", True))

        if self.state.phase == "manual":
            self.renderstate.set_prop(("current_page", ManualPhasePage))
        elif self.state.phase == "game":
            self.renderstate.set_prop(("current_page", GamePage))

    def credit_handler(self):
        from .credit_page import CreditPage
        self.renderstate.set_prop(("current_page", CreditPage))

    def exit_handler(self):
        popup = r.PopupPrompt(self.term, self.renderstate, "Are you sure?", [("Yup", lambda e: exit(0)), ("Nah", lambda e: e)])
        self.renderstate.set_prop(("current_popup", popup))