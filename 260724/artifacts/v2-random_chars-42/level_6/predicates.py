def ach_collect_sgqeje(state, *args):
    """True once at least one sgqeje collection achievement is recorded."""
    return state.get("ach_collect_sgqeje", 0) > 0


def ach_collect_tpkhxk(state, *args):
    """True once at least one tpkhxk collection achievement is recorded."""
    return state.get("ach_collect_tpkhxk", 0) > 0


def ach_make_sgqeje_bcwrvm(state, *args):
    """True once an sgqeje_bcwrvm item has been crafted."""
    return state.get("ach_make_sgqeje_bcwrvm", 0) > 0


def ach_make_tpkhxk_bcwrvm(state, *args):
    """True once a tpkhxk_bcwrvm item has been crafted."""
    return state.get("ach_make_tpkhxk_bcwrvm", 0) > 0


def ach_make_tpkhxk_wqiqzh(state, *args):
    """True once a tpkhxk_wqiqzh item has been crafted."""
    return state.get("ach_make_tpkhxk_wqiqzh", 0) > 0


def ach_place_sgqeje(state, *args):
    """True once an sgqeje entity has been placed."""
    return state.get("ach_place_sgqeje", 0) > 0


def ach_place_zezroc(state, *args):
    """True once a zezroc entity has been placed."""
    return state.get("ach_place_zezroc", 0) > 0


def inv_sgqeje_ge1(state, *args):
    """True when the player has at least one sgqeje in inventory."""
    return state.get("inv_sgqeje", 0) >= 1


def inv_sgqeje_ge2(state, *args):
    """True when the player has at least two sgqeje in inventory."""
    return state.get("inv_sgqeje", 0) >= 2