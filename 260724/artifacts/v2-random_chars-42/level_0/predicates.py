def is_set(state, *args):
    """True when the specified status/achievement flag is set."""
    if not args:
        return False
    flag = args[0]
    return bool(state.get(flag, 0))