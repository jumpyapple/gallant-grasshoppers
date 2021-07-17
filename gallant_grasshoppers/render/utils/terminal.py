from blessed import Terminal

term = Terminal()  # Reuse this object instead of creating a new one.


def get_term() -> Terminal:
    """Get Terminal Object"""
    return term
