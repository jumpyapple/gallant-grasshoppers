from .styleTypes import styles
from .utils.terminal import get_term as terminal


class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(self, window: object, begin_x: int = 0, begin_y: int = 0, children: list[any] = None,
                 selectable: bool = False, id: str = None):
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
        if window:
            self.window = window
            self.begin_x += window.begin_x
            self.begin_y += window.begin_y

    def get_id(self) -> str:
        """Gets Id"""
        return self.id

    def get_children(self) -> any:
        """Gets components children"""
        return self.children

    def is_selectable(self) -> bool:
        """Returns Bool whether component is selectable"""
        return self.selectable

    def set_callback(self, func: any, var: any) -> None:
        """Sets callback function to be executed when selected"""
        self.callback = (func, var)

    def select(self) -> None:
        """Exectues callback function"""
        func = self.callback[0]
        if self.callback[1]:
            func(self.callback[1])
            return
        func()

    def __repr__(self):
        text = ""
        if self.styles:
            keys = self.styles.keys()
            for key in keys:
                text += styles[key](self, self.styles[key])
        for c, line in enumerate(self.children):
            text += (self.terminal.move_xy(self.begin_x, self.begin_y + c)) + str(line)
        return text

    def set_styles(self, stylesjson: dict) -> None:
        """Sets styleTypes for a component"""
        self.styles = stylesjson

    def set_children(self, children: list[any] = None) -> bool:
        """Sets data for to be displayed in component"""
        self.children = children
        return True

    def draw_component(self) -> bool:
        """Draws component"""
        print(self)
        return True

    def set_wh(self, width: int = 0, height: int = 5,) -> None:
        """Set width and height"""
        self.width = width
        self.height = height
