def adjacent_to(state, *args):
    """True when the actor occupies a cell cardinally adjacent to the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = state.get(who, [])
    resource_positions = state.get(what, [])

    if not isinstance(actor_positions, (list, tuple)):
        return False
    if not isinstance(resource_positions, (list, tuple)):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) != 2:
            continue
        for resource_pos in resource_positions:
            if not isinstance(resource_pos, (list, tuple)) or len(resource_pos) != 2:
                continue
            if abs(actor_pos[0] - resource_pos[0]) + abs(actor_pos[1] - resource_pos[1]) == 1:
                return True

    return False