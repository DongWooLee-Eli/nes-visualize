def ach_collect_sgqeje(state, *args):
    """True once sgqeje has been collected."""
    return state.get("ach_collect_sgqeje", 0) > 0


def ach_collect_tpkhxk(state, *args):
    """True once tpkhxk has been collected."""
    return state.get("ach_collect_tpkhxk", 0) > 0


def ach_make_tpkhxk_bcwrvm(state, *args):
    """True once a tpkhxk_bcwrvm item has been crafted."""
    return state.get("ach_make_tpkhxk_bcwrvm", 0) > 0


def ach_make_tpkhxk_wqiqzh(state, *args):
    """True once a tpkhxk_wqiqzh item has been crafted."""
    return state.get("ach_make_tpkhxk_wqiqzh", 0) > 0


def ach_place_sgqeje(state, *args):
    """True once sgqeje has been placed."""
    return state.get("ach_place_sgqeje", 0) > 0


def ach_place_zezroc(state, *args):
    """True once zezroc has been placed."""
    return state.get("ach_place_zezroc", 0) > 0


def inv_sgqeje_ge1(state, *args):
    """True when the inventory contains at least one sgqeje."""
    return state.get("inv_sgqeje", 0) >= 1


def inv_sgqeje_ge2(state, *args):
    """True when the inventory contains at least two sgqeje."""
    return state.get("inv_sgqeje", 0) >= 2