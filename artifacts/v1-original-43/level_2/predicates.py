def is_set(state, *args):
    """True when the requested status/achievement flag has been set."""
    if not args:
        return False

    flag = args[0]
    if bool(state.get(flag, False)):
        return True

    # Crafting updates inventory in the low-level model rather than the
    # corresponding achievement flag.
    if isinstance(flag, str) and flag.startswith("ach_make_"):
        product = flag[len("ach_make_"):]
        return state.get("inv_" + product, 0) > 0

    return False


def wood_accessible(state, *args):
    """True when the actor exists and at least one tree source remains."""
    if len(args) < 2:
        return False

    who, trees = args[0], args[1]
    return bool(state.get(who)) and bool(state.get(trees))