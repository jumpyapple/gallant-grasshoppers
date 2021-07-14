
def get_selectables(c: object) -> list[object]:
    """Gets selectable components"""
    try:
        if c.selectables:
            selects = c.selectables
            for i in c.selectables:
                selects += get_selectables(c.selectables)
            return selects
    except AttributeError:
        return []
    return []
