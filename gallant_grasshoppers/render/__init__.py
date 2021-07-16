from blessed import Terminal

from .component import Component, PopupPrompt, PopupMessage  # noqa: F401
from .utils.get_selectables import get_selectables  # noqa: F401
from .utils.terminal import get_term


def terminal() -> Terminal:
    """Gets Terminal"""
    return get_term()
