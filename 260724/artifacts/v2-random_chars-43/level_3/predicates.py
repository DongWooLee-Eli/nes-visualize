def is_made(state, *args):
    """True when the specified make-status achievement has been completed."""
    if not args:
        return False
    return bool(state.get(args[0], 0))


def is_placed(state, *args):
    """True when the specified place-status achievement has been completed."""
    if not args:
        return False
    return bool(state.get(args[0], 0))