def ach_place_zezroc(state, *args):
    """True when the zezroc placement achievement has been completed."""
    return bool(state.get("ach_place_zezroc", 0))


def has_two_tpkhxk(state, *args):
    """True when the player has at least two tpkhxk items."""
    return state.get("inv_tpkhxk", 0) >= 2