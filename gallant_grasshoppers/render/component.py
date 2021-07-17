import io
import sys
from typing import Any, Callable, Union

from blessed import Terminal
from blessed.formatters import FormattingString, NullCallableString
from blessed.keyboard import Keystroke
from render.utils import StateManager

from .styleTypes import bg_color, color, styles
from .utils.terminal import get_term as terminal


class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(
        self,
        window: object,
        begin_x: int = 0,
        begin_y: int = 0,
        children: list[any] = None,
        selectable: bool = False,
        id: str = None,
    ):
        """
        Parameters

        window : obj
            A component object or terminal object
        width : int
            How wide the component is.
            (Default is 5 spaces wide)
        height : int
            How tall the component is.
            (Default is 5 spaces high)
        begin_x : int
            Where the top left starts on the X axis
            (Default is 0)
        begin_y : int
            Where the top left starts on the Y axis
            (Default is 0)
        data : any
            Whatever you want the data to be inside. Could be components, strs, ints, etc
            IF STR: put in list to be displayed on single line. i.e. ["Hello World!"]
            (Default is None)
        """
        self.terminal = terminal()
        self.height = self.terminal.height
        self.width = self.terminal.width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.selectable = selectable
        self.children = children
        self.styles = None
        self.id = id
        self.callback = None
        self.window = window
        if window:
            self.styles = self.window.styles
            self.begin_x += window.begin_x
            self.begin_y += window.begin_y
            self.width = self.window.width
            self.height = self.window.height

    def get_id(self) -> str:
        """Gets Id"""
        return self.id

    def get_children(self) -> any:
        """Gets components children"""
        return self.children

    def is_selectable(self) -> bool:
        """Returns Bool whether component is selectable"""
        return self.selectable

    def set_callback(self, func: Callable[..., None], *args, **kwargs) -> None:
        """Sets callback function to be executed when selected"""
        self.callback = (func, args, kwargs)

    def select(self) -> None:
        """Exectues callback function"""
        # jumpyapple: we can use *args to unpack the list of arguments
        # to be passed to the function.
        # Oh I see why you are using tuple in StateManager.set_prop now.
        func, args, kwargs = self.callback
        func(*args, **kwargs)

    def __repr__(self):
        text = self.terminal.normal
        if self.styles:
            keys = self.styles.keys()
            for key in keys:
                output = styles[key](self, self.styles[key])
                if output:
                    text += output

        # Write out text
        for c, line in enumerate(self.children):
            if self.begin_x is None and self.begin_y is None:
                text += self.terminal.move_xy(
                    self.window.begin_x, self.window.begin_y + c
                ) + str(line)
                continue
            line = str(line) + (self.width - len(str(line)) - 2) * " "
            text += self.terminal.move_xy(self.begin_x, self.begin_y + c) + str(line)

        next_text = self.terminal.normal
        if self.window is not None and self.window.styles:
            try:
                if self.window.styles["color"]:
                    next_text = color(self, self.window.styles["color"])

                if self.window.styles["bg-color"]:
                    next_text += bg_color(self, self.window.styles["bg-color"])
            except KeyError:
                pass
        return text + next_text

    def set_styles(self, stylesjson: dict) -> None:
        """Sets styleTypes for a component"""
        self.styles = stylesjson

    def set_children(self, children: list[any] = None) -> bool:
        """Sets data for to be displayed in component"""
        self.children = children
        return True

    def draw_component(self) -> bool:
        """Draws component"""
        old_stdout = sys.stdout  # all this buffers the output so it can
        new_stdout = io.StringIO()  # come out all at once and the screen doesn't blink
        sys.stdout = new_stdout
        print(self.terminal.clear())
        print(self)
        sys.stdout = old_stdout
        print(new_stdout.getvalue())

        return True

    def set_wh(self, width: int = 0, height: int = 5,) -> None:
        """Set width and height"""
        self.width = width
        self.height = height


class PopupMessage:
    """
    Represent a popup object.

    :param term: The `blessed.Terminal` object.
    :param render_state: The `StateManager` object.
    :param message: The message to be displayed.
    :param y: The y position of the popup middle line.
    :param style: The style of the popup.
    :param dismiss_key_name: The name of the key to dismiss the popup. If `auto_dismiss` is True, this is ignored.
    :param auto_dismiss: If True, the popup will be removed after the render function is called
    more than `dismiss_after` times.
    :param dismiss_after: The amount of ticks before the popup is removed.
    """

    def __init__(
        self,
        term: Terminal,
        render_state: StateManager,
        message: str,
        y: Union[int, Any] = None,
        style: Union[FormattingString, NullCallableString] = None,
        dismiss_key_name: str = "KEY_ESCAPE",
        auto_dismiss: bool = True,
        dismiss_after: int = 4,
    ) -> None:
        self.term = term
        self.render_state = render_state
        self.message = message
        self.dismiss_key_name = dismiss_key_name
        self.auto_dismiss = auto_dismiss
        self.dismiss_after = dismiss_after
        self.ticks = 0

        self.y = y
        if self.y is None:
            self.y = term.height // 2

        self.style = style
        if self.style is None:
            self.style = self.term.formatter("black_on_cyan3")

    def render(self) -> None:
        """Render the popup message."""
        # Assume that this got call every `tick` in the main loop.
        if self.auto_dismiss:
            self.ticks += 1
            if self.ticks > self.dismiss_after:
                self.render_state.set_prop(("current_popup", None))

        term = self.term
        full_width = self.style(" " * term.width)
        with term.cbreak(), term.hidden_cursor(), term.location(0, self.y):
            print(term.move_up + full_width)
            print(self.style(term.center(self.message)))
            print(full_width)

    def handle_input(self, key: Union[str, Keystroke]) -> None:
        """Handling the input"""
        if getattr(key, "is_sequence", None) is not None:
            if key.name == self.dismiss_key_name:
                self.render_state.set_prop(("current_popup", None))
        elif key:
            if key == self.dismiss_key_name:
                self.render_state.set_prop(("current_popup", None))


class PopupPrompt(PopupMessage):
    """
    Represent a popup object.

    :param term: The `blessed.Terminal` object.
    :param render_state: The `StateManager` object.
    :param message: The message to be displayed.
    :param choices: The list of 2-tuple contains word and callback function.
    :param kwargs: See kwargs of `PopupMessage` for detail.
    """

    def __init__(
        self,
        term: Terminal,
        render_state: StateManager,
        message: str,
        choices: list[tuple],
        **kwargs,
    ) -> None:
        super().__init__(term, render_state, message, **kwargs)
        self.choices = choices

        self.callbacks = []

        choices = []
        for choice, func in self.choices:
            first_char = choice[0]
            choices.append(f"[{first_char}]{choice[1:]}")

            self.callbacks.append((first_char.lower(), func))
        self.choice_text = " ".join(choices)

    def render(self) -> None:
        """Render the popup prompt."""
        term = self.term

        full_width = self.style(" " * term.width)
        with term.cbreak(), term.hidden_cursor(), term.location(0, self.y):
            print(term.move_up + full_width)
            print(self.style(term.center(self.message)))
            print(self.style(term.center(self.choice_text)))
            print(full_width)

    def handle_input(self, key: Union[str, Keystroke]) -> None:
        """Handling the input"""
        if getattr(key, "is_sequence", None) is not None:
            if key.name == self.dismiss_key_name:
                self.render_state.set_prop(("current_popup", None))
                return
            for first_char, func in self.callbacks:
                if key == first_char:
                    self.render_state.set_prop(("current_popup", None))
                    func("")
                    return
        elif key:
            for first_char, func in self.callbacks:
                if key == first_char:
                    self.render_state.set_prop(("current_popup", None))
                    func("")
                    break
