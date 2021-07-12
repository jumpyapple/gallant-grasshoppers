from .start_page import print_start_page

from blessed import Terminal

from .utils.terminal import get_term




def terminal() -> Terminal:
    """Gets Terminal"""
    return get_term()
