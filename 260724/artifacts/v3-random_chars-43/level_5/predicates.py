def ach_collect_sgqeje(state, *args):
    """True when the sgqeje collection achievement has been recorded."""
    return bool(state.get("ach_collect_sgqeje", 0))


def ach_collect_tpkhxk(state, *args):
    """True when the tpkhxk collection achievement has been recorded."""
    return bool(state.get("ach_collect_tpkhxk", 0))


def ach_place_sgqeje(state, *args):
    """True when the sgqeje placement achievement has been recorded."""
    return bool(state.get("ach_place_sgqeje", 0))