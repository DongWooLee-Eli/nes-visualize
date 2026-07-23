def placed_sgqeje(state, *args):
    """True when placing sgqeje has been achieved."""
    return state.get("ach_place_sgqeje", 0) > 0