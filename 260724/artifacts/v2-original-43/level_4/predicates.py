def achieved(state, *args):
    """True when the specified achievement has been completed."""
    if not args:
        return False
    result = args[0]
    return bool(state.get(result, 0))


def stone(state, *args):
    """True when the specified stone resource still exists in the world."""
    if not args:
        return False
    target = args[0]
    return bool(state.get(target, []))


def tree(state, *args):
    """True when the specified tree resource still exists in the world."""
    if not args:
        return False
    target = args[0]
    return bool(state.get(target, []))