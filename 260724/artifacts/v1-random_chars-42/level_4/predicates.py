def is_achieved(state, *args):
    """True when the requested achievement status has been attained."""
    if not args:
        return False
    result = args[0]
    return bool(state.get(result, 0))


def is_present(state, *args):
    """True when the target item is present in the world."""
    if not args:
        return False
    target = args[0]
    return bool(state.get(target, []))