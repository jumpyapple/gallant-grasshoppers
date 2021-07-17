from ..utils.terminal import term


def bg_color(component: object, param: any = None) -> str:
    """Changes colors in component"""
    if not param:
        return ""
    return term.on_color_rgb(param[0], param[1], param[2])
