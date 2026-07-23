def sword_made(state, *args):
    """True when the requested sword-making achievement has been completed."""
    result = args[0] if args else "ach_make_wood_sword"
    achievement_key = str(result)

    if state.get(achievement_key, 0) > 0:
        return True

    # The low-level model may expose the crafted item directly.
    if achievement_key == "ach_make_wood_sword":
        return state.get("inv_wood_sword", 0) > 0

    return False


def table_placed(state, *args):
    """True when the requested table-placement achievement is complete."""
    result = args[0] if args else "ach_place_table"
    achievement_key = str(result)

    if state.get(achievement_key, 0) > 0:
        return True

    # A placed table may also be represented as a nonempty spatial layer.
    if achievement_key == "ach_place_table":
        return bool(state.get("table", []))

    return False


def wood_available(state, *args):
    """True when the requested wood source exists in the world."""
    source = str(args[0]) if args else "tree"
    value = state.get(source)
    return isinstance(value, (list, tuple, set, dict)) and bool(value)