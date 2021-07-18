from . import term
from .utils import longest


def bg_color(component: object, param: any = None) -> str:
    """Changes colors in component"""
    if not param:
        return ""
    return term.on_color_rgb(param[0], param[1], param[2])


def border(component: object, param: any = None) -> str:
    """Draws border around component"""
    # height = 0
    # width = 0
    if not param:
        return ""
    terminal = term
    border_text = ""
    for i in range(component.height):
        border_text += terminal.move_xy(component.begin_x, component.begin_y + i) + "│"
        border_text += (
            terminal.move_xy(
                component.begin_x + component.width - 1, component.begin_y + i
            )
            + "│"
        )
    border_text += (
        terminal.move_xy(component.begin_x, component.begin_y) + "─" * component.width
    )
    border_text += (
        terminal.move_xy(component.begin_x, component.begin_y + component.height - 1)
        + "─" * component.width
    )

    border_text += (
        terminal.move_xy(component.begin_x + component.width - 1, component.begin_y)
        + "┐"
    )
    border_text += terminal.move_xy(component.begin_x, component.begin_y) + "┌"
    border_text += (
        terminal.move_xy(component.begin_x, component.begin_y + component.height - 1)
        + "└"
    )
    border_text += (
        terminal.move_xy(
            component.begin_x + component.width - 1,
            component.begin_y + component.height - 1,
        )
        + "┘"
    )

    component.begin_x += 1
    component.begin_y += 1

    return border_text


def center(component: object, param: any = None) -> None:
    """Centers items in components"""
    if not param:
        return

    longest_length = longest(component)

    for c, i in enumerate(component.children):
        spaces = (longest_length - len(str(i))) // 2 + (
            component.width - longest_length
        ) // 2
        component.children[c] = " " * spaces + str(component.children[c])

    return


def color(component: object, param: any = None) -> str:
    """Changes colors in component"""
    if not param:
        return ""
    return term.color_rgb(param[0], param[1], param[2])


styles = {
    "color": color,
    "bg-color": bg_color,
    "center": center,
    "border": border,
    "margin": None,
    "padding": None,
}
