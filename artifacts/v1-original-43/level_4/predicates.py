def is_set(state, *args):
    """True when the specified status/achievement flag has been set."""
    if not args:
        return False
    flag = args[0]
    return bool(state.get(flag, 0))


def stone_accessible(state, *args):
    """True when the actor exists and the specified stone source is available."""
    if len(args) < 2:
        return False
    who, stones = args[0], args[1]
    return bool(state.get(who)) and bool(state.get(stones))


def wood_accessible(state, *args):
    """True when the actor exists and the specified tree source is available."""
    if len(args) < 2:
        return False
    who, trees = args[0], args[1]
    return bool(state.get(who)) and bool(state.get(trees))