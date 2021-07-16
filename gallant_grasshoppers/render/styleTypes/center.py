from ..utils.longest import longest

# GOING TO HAVE TO MOVE THIS OUT INTO COMPONENT


def center(component: object, param: any = None) -> None:
    """Centers items in components"""
    if not param:
        return

    longest_length = longest(component)

    for c, i in enumerate(component.children):
        spaces = longest_length - len(i) // 2
        component.children[c] = " "*spaces+component.children[c]

    return
