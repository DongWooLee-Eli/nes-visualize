def ach_collect_tpkhxk(state, *args):
    """True once tpkhxk has been collected."""
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


def ach_make_tpkhxk_wqiqzh(state, *args):
    """True once a tpkhxk_wqiqzh item has been crafted."""
    return bool(
        state.get("ach_make_tpkhxk_wqiqzh", 0)
        or state.get("inv_tpkhxk_wqiqzh", 0) > 0
    )


def ach_place_zezroc(state, *args):
    """True once a zezroc structure has been placed."""
    return bool(
        state.get("ach_place_zezroc", 0)
        or state.get("zezroc", [])
    )