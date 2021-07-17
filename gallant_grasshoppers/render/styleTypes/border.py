from ..utils.terminal import term


def border(component: object, param: any = None) -> str:
    """Draws border around component"""
    # height = 0
    # width = 0
    if not param:
        return ""
    terminal = term
    border = ""
    for i in range(component.height):
        border += terminal.move_xy(component.begin_x, component.begin_y + i) + "│"
        border += terminal.move_xy(component.begin_x + component.width - 1, component.begin_y + i) + "│"
    border += terminal.move_xy(component.begin_x, component.begin_y) + "─" * component.width
    border += terminal.move_xy(component.begin_x, component.begin_y + component.height - 1) + "─" * component.width

    border += terminal.move_xy(component.begin_x + component.width - 1, component.begin_y) + "┐"
    border += terminal.move_xy(component.begin_x, component.begin_y) + "┌"
    border += terminal.move_xy(component.begin_x, component.begin_y + component.height - 1) + "└"
    border += terminal.move_xy(component.begin_x + component.width - 1, component.begin_y + component.height - 1) + "┘"

    component.begin_x += 1
    component.begin_y += 1

    return border
