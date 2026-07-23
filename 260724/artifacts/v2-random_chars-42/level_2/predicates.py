def ach_collect_tpkhxk(state, *args):
    """True once tpkhxk has been collected or its achievement flag is set."""
    return bool(
        state.get("ach_collect_tpkhxk", 0)
        or state.get("inv_tpkhxk", 0) > 0
    )


def ach_make_tpkhxk_bcwrvm(state, *args):
    """True once a tpkhxk_bcwrvm item has been crafted."""
    return bool(
        state.get("ach_make_tpkhxk_bcwrvm", 0)
        or state.get("inv_tpkhxk_bcwrvm", 0) > 0
    )


def ach_place_zezroc(state, *args):
    """True once a zezroc has been placed in the world."""
    return bool(
        state.get("ach_place_zezroc", 0)
        or state.get("zezroc", [])
    )