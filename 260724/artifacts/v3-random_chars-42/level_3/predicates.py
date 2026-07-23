def zezroc_placed(state, *args):
    """True when the zezroc placement achievement has been completed."""
    return bool(state.get("ach_place_zezroc", 0))