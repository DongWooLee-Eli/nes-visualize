def ach_make_sgqeje_bcwrvm(state, *args):
    """True when the sgqeje_bcwrvm crafting achievement has been attained."""
    return bool(
        state.get("ach_make_sgqeje_bcwrvm", 0)
        or state.get("inv_sgqeje_bcwrvm", 0) > 0
    )