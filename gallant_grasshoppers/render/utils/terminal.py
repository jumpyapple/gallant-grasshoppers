from blessed import Terminal

# We will be reusing this object
# instead of creating a new one.
term = Terminal()

def get_term() -> Terminal:
    """Get Terminal Object"""
    return term
