def ach_place_table(state, *args):
    """True when a table has been placed or its achievement flag is set."""
    if bool(state.get("ach_place_table", 0)):
        return True

    return any(
        key.endswith("table") and isinstance(value, list) and bool(value)
        for key, value in state.items()
    )


def close_to(state, *args):
    """True when the specified actor is adjacent to the specified resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = state.get(who, [])
    resource_positions = state.get(what, [])

    if not isinstance(actor_positions, list) or not isinstance(resource_positions, list):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) < 2:
            continue
        for resource_pos in resource_positions:
            if not isinstance(resource_pos, (list, tuple)) or len(resource_pos) < 2:
                continue
            if max(
                abs(actor_pos[0] - resource_pos[0]),
                abs(actor_pos[1] - resource_pos[1]),
            ) <= 1:
                return True

    return False