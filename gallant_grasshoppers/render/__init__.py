from blessed import Terminal

term = Terminal()

# E402 is needed for circular import.
from .component import Component, PopupMessage, PopupPrompt  # noqa: F401, E402
from .utils.get_selectables import get_selectables  # noqa: F401, E402
