def ach_collect_wood(state, *args):
    """True once wood collection is recorded or its products provide evidence."""
    return bool(
        state.get("ach_collect_wood", 0)
        or state.get("inv_wood", 0) > 0
        or state.get("inv_wood_pickaxe", 0) > 0
        or any(
            key.endswith("table") and bool(value)
            for key, value in state.items()
        )
    )


def ach_make_wood_pickaxe(state, *args):
    """True once a wooden pickaxe has been made."""
    return bool(
        state.get("ach_make_wood_pickaxe", 0)
        or state.get("inv_wood_pickaxe", 0) > 0
    )


def ach_place_table(state, *args):
    """True once table placement is recorded or a table exists in the world."""
    return bool(
        state.get("ach_place_table", 0)
        or any(
            key.endswith("table") and bool(value)
            for key, value in state.items()
        )
    )