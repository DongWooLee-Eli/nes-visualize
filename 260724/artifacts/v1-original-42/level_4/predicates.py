def achievement_reached(state, *args):
    """True when the requested achievement has been earned."""
    if not args:
        return False

    flag = args[0]
    if bool(state.get(flag, 0)):
        return True

    # Collection achievements can also be inferred from inventory because the
    # low-level transition model does not update every achievement counter.
    prefix = "ach_collect_"
    if isinstance(flag, str) and flag.startswith(prefix):
        resource = flag[len(prefix):]
        return state.get("inv_" + resource, 0) > 0

    return False


def resource_available(state, *args):
    """True when at least one instance of the requested resource exists."""
    if not args:
        return False

    item = args[0]
    value = state.get(item)

    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    if isinstance(value, (int, float)):
        return value > 0
    return bool(value)