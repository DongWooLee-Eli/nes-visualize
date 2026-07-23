def ach_collect_wood(state, *args):
    """True once wood collection is recorded or evidenced by wood-derived items."""
    return bool(
        state.get("ach_collect_wood", 0)
        or state.get("inv_wood", 0) > 0
        or state.get("inv_wood_pickaxe", 0) > 0
        or state.get("inv_wood_sword", 0) > 0
        or ach_place_table(state)
    )


def ach_make_wood_pickaxe(state, *args):
    """True once a wooden pickaxe has been crafted."""
    return bool(
        state.get("ach_make_wood_pickaxe", 0)
        or state.get("inv_wood_pickaxe", 0) > 0
    )


def ach_make_wood_sword(state, *args):
    """True once a wooden sword has been crafted."""
    return bool(
        state.get("ach_make_wood_sword", 0)
        or state.get("inv_wood_sword", 0) > 0
    )


def ach_place_table(state, *args):
    """True once table placement is recorded or a table exists in the world."""
    if state.get("ach_place_table", 0):
        return True

    return any(
        key.endswith("table") and isinstance(value, list) and bool(value)
        for key, value in state.items()
    )