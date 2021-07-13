from .styleTypes import styles
from .utils.terminal import get_term as terminal


class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(
            self, window: object = terminal(),
            begin_x: int = 0, begin_y: int = 0, data: any = None,
            width: int = 5, height: int = 5,):
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
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.styles = None
        self.data = data
        if window:
            self.window = window
            self.begin_x += window.begin_x
            self.begin_y += window.begin_y

    def __repr__(self):
        text = ""
        keys = self.styles.keys()
        for key in keys:
            text += styles[key](self, self.styles[key])
        for c, line in enumerate(self.data):
            text += (self.terminal.move_xy(self.begin_x, self.begin_y + c)) + str(line)
        return text

    def set_styles(self, stylesjson: dict) -> None:
        """Sets styles for a component"""
        self.styles = stylesjson

    def set_data(self, data: any = None) -> bool:
        """Sets data for to be displayed in component"""
        self.data = data
        return True

    def draw_component(self) -> bool:
        """Draws component"""
        print(self)
        return True


if __name__ == '__main__':
    win = Component(None, 1, 2, 3, 4)
    print(win)
