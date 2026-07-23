def is_achieved(state, *args):
    """True when the specified status has a truthy achievement value."""
    if not args:
        return False
    flag = args[0]
    return bool(state.get(flag, False))


def is_available(state, *args):
    """True when at least one instance of the specified resource remains."""
    if not args:
        return False
    item = args[0]
    return bool(state.get(item, False))