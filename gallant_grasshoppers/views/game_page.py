#!/usr/bin/env python3
import render as r  # ignore this. it is correct syntax
from blessed import Terminal

from . import BasePage

Component = r.Component


class GamePage(BasePage):
    """A game page."""

    def __init__(self, state: object, term: Terminal, renderstate: object):
        super().__init__(state, term, renderstate)
        self.comps = []
        self.current_cursor = None
        self.current_options = None
        self.menus = [self.state.available_generators, self.state.available_upgrades]
        self.current_menu = renderstate["current_menu"]
        self.main = self.renderstate["head_component"]
        self.main.set_styles({"color": [204, 153, 0], "bg-color": [102, 51, 0]})
        left_half = Component(self.main, 0, 0)
        left_half.set_wh(self.main.width // 2, self.main.height)
        left_half.set_styles({"color": [204, 153, 0], "bg-color": [102, 51, 0], "border": True})

        def component_constructor(data: any, location: tuple, letter: str) -> Component:
            """Constructs components"""
            id = f"{data['ID']}"
            desc = f"{data['DESCRIPTION']}"
            try:
                curr = {self.state.state['generators'][data['ID']]['amount']}
            except KeyError:
                curr = 0
            bpt = f"BPS: {data['BPT']} PRICE:{data['COST']} CURRENT: {curr}"

            c = Component(left_half, location[0] - int(left_half.width // 1.5) // 2, location[1],
                          children=[letter, id, desc, bpt])
            c.set_wh(int(left_half.width // 1.5), len(c.children) + 2)

            for count, i in enumerate(c.children):
                if len(i) > c.width-2:
                    c.children[count] = i[:c.width - 2]
                    c.children.insert(count + 1, i[c.width - 3:])
                    c.height += 1

            c.set_styles(
                {
                    "color": [204, 153, 0],
                    "bg-color": [102, 51, 0],
                    "border": True,
                    "center": True,
                }
            )
            return c
        # print(str(self.state.state["generators"]))

        # placeholder info for map
        to_be_comps = self.current_menu[:4]
        self.current_options = to_be_comps
        letters = ["Q", "W", "E", "R"]
        loc_list = [(left_half.width // 2 - len(i) // 2, c*10 + 10 + left_half.height // 10)
                    for c, i in enumerate(to_be_comps)]

        list_of_comps = map(component_constructor, to_be_comps, loc_list,
                            [letters[c] for c, i in enumerate(to_be_comps)])
        menu_items = Component(left_half, 1, 1)
        menu_items.height = left_half.height // 10
        menu_items.set_children([Component(menu_items, 0, left_half.height // 20,
                                           [str(c+1), "", i] + ["" for _ in range(left_half.height // 20 - 3)])
                                 for c, i in enumerate(["GENERATORS", "UPGRADES", "ACHIEVEMENTS", "OPTIONS"])])

        for c, i in enumerate(menu_items.children):
            i.begin_x = int((menu_items.width // 6) * c * 1.5 + (menu_items.width // 24))
            i.set_styles({"color": [204, 153, 0], "bg-color": [102, 51, 0], "border": True, "center": True})

        for i in menu_items.children:
            i.width = menu_items.width // 5
        c_list = list(list_of_comps) + menu_items.children
        left_half.set_children(c_list)

        right_half = Component(self.main, self.main.width // 2, 0)
        right_half.set_wh(self.main.width // 2, self.main.height)
        right_half.set_styles({"border": True})

        current_cash = self.state.getCash()
        curr_string = f"Boxes Folded: {current_cash}"

        self.c = Component(
            right_half,
            1,
            right_half.height // 5,
            children=[curr_string],
            selectable=False,
        )
        self.c.set_styles({"center": True})
        self.renderstate["total_boxes_c"] = c
        update_box = Component(right_half, 1, right_half.height // 2, children=[""])
        update_box.set_wh(right_half.width - 2, right_half.height // 2 - 1)
        update_box.set_styles({"border": True})
        right_half.set_children([self.c, update_box])
        self.main.set_children([left_half, right_half])

    def render(self) -> None:
        """Render the game page."""
        current_cash = self.state.getCash()
        curr_string = f"Boxes Folded: {current_cash}"
        self.c.set_children([curr_string])

        self.main.draw_component()

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        nav_menu = ["1", "2", "3", "4"]
        game_menu = ["q", "w", "e", "r"]
        if key == " ":
            self.state.makeBox()
        if key in nav_menu:
            self.renderstate["current_menu"] = self.menus[nav_menu.index(key)]
        if key in game_menu:
            self.state.buyGenerator(self.current_options[game_menu.index(key)]['ID'])
        if key == "5":
            # Save the session.
            self.state.saveGame()
            self.renderstate["is_exiting"] = True
            self.renderstate["is_in_game"] = False
