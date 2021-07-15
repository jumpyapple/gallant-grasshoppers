
import render as r  # ignore this. it is correct syntax
from blessed import Terminal

term = Terminal()
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


def print_test_page(**kwargs) -> None:
    """Creates start page, can be called from signal module and directly"""
    main = Component(None)
    c = Component(main, term.width // 2 - len(boxer_logo[1])//2,
                  term.height // 3, children=boxer_logo, selectable=False)
    c.set_wh(5, 5)
    c2 = Component(main, term.width // 2, term.height - 1, ["Exit"], selectable=True, id="exit")
    c2.set_wh(1, 1)
    c3 = Component(main, term.width // 2, term.height - 4, ["Next Page"], selectable=True, id="next")
    c3.set_wh(1, 1)
    c2.set_callback(exit, 0)
    c3.set_callback(kwargs["main"].set_prop, ("current_page", print_page2))
    main.set_children([c, c3, c2])
    children = main.get_children()
    comps = []
    for i in children:
        if isinstance(i, Component) and i.is_selectable():
            comps.append(i)

    current_cursor = comps[0]

    for i in comps:
        try:
            if kwargs["main"].get_prop("cursor").get_id() == i.get_id():
                current_cursor = i
                break
        except AttributeError:
            break

    current_cursor.set_styles({"border": True})

    main.draw_component()

    if kwargs["keypress"] == " ":
        current_cursor.select()
    elif kwargs["keypress"] and kwargs["keypress"].is_sequence:
        if kwargs["keypress"].name == "KEY_DOWN":
            current_cursor = comps[(comps.index(current_cursor)+1) % len(comps)]
            kwargs["main"].set_prop(("cursor", current_cursor))
        elif kwargs["keypress"].name == "KEY_UP":
            current_cursor = comps[comps.index(current_cursor)-1]
            kwargs["main"].set_prop(("cursor", current_cursor))


def print_page2(**kwargs) -> None:
    """Test print page test 2"""
    c2 = Component(None, term.width // 2, term.height - 1, ["page2"])
    c2.draw_component()
