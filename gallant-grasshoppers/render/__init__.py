from blessed import Terminal

from .component import Component  # noqa: F401
from .utils.terminal import get_term


def terminal() -> Terminal:
    """Gets Terminal"""
    return get_term()
