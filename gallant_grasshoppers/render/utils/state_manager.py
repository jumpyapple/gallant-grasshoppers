class StateManager:
    """Controls current page data"""

    def __init__(self, state: dict) -> None:
        """Inits page"""
        self.state = state

    def set_state(self, state: dict) -> None:
        """Sets current page"""
        self.state = state

    def get_state(self) -> any:
        """Returns current page"""
        return self.state

    def get_prop(self, prop: str) -> any:
        """Gets property information"""
        try:
            return self.state[prop]
        except KeyError:
            return False

    def set_prop(self, d: tuple) -> None:
        """Sets Property information"""
        self.state[d[0]] = d[1]
