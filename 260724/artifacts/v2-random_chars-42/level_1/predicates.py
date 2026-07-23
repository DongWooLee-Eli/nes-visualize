def ach_collect_tpkhxk(state, *args):
    """True when tpkhxk has been collected or is currently in inventory."""
    return bool(
        state.get("ach_collect_tpkhxk", 0)
        or state.get("inv_tpkhxk", 0) > 0
    )


def ach_place_zezroc(state, *args):
    """True when zezroc has been placed or its placement achievement is set."""
    return bool(
        state.get("ach_place_zezroc", 0)
        or state.get("zezroc", [])
    )