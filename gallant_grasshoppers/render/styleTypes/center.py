from ..utils.longest import longest


def center(component: object, param: any = None) -> None:
    """Centers items in components"""
    if not param:
        return

    longest_length = longest(component)

    for c, i in enumerate(component.children):
        spaces = (longest_length - len(str(i))) // 2 + (component.width-longest_length) // 2 - 1
        component.children[c] = " "*spaces+str(component.children[c])

    return
