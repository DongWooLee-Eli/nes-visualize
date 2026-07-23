def ach_collect_tpkhxk(state, *args):
    """True when the tpkhxk collection achievement has been completed."""
    return bool(state.get("ach_collect_tpkhxk", 0))