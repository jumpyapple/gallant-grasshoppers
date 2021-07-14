
import render as r  # ignore this. it is correct syntax
from blessed import Terminal

term = Terminal()
Component = r.Component


def print_test_page(**kwargs) -> None:
    """Creates start page, can be called from signal module and directly"""
    main = Component(None)
    c = Component(main, term.width // 2,
                  term.height // 3, data=[str(kwargs["frame"])])
    c.set_wh(5, 5)
    c.set_styles({"border": True})
    c2 = Component(main, term.width // 2, term.height - 1, [str(kwargs["keypress"])])
    c2.set_wh(10, 5)
    c2.set_callback(kwargs["current_page"], print_page2)
    main.set_data([c, c2])
    main.set_selectables([c2])
    c2.set_selected(True)
    selectables = r.get_selectables(main)

    current_cursor = False

    for i in selectables:
        if i.get_selected():
            current_cursor = i
            break
    if not current_cursor:
        current_cursor = selectables[0]

    current_cursor.set_styles({"border": True})

    if kwargs["keypress"] == "h":
        c2.select()

    main.draw_component()


def print_page2(**kwargs) -> None:
    """Test print page test 2"""
    c2 = Component(None, term.width // 2, term.height - 1, ["page2"])
    c2.draw_component()
