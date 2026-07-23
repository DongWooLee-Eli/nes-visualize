def close_to(state, *args):
    """True when the actor is on or orthogonally adjacent to the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = state.get(who, [])
    resource_positions = state.get(what, [])

    if not isinstance(actor_positions, list) or not isinstance(resource_positions, list):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) != 2:
            continue

        for resource_pos in resource_positions:
            if not isinstance(resource_pos, (list, tuple)) or len(resource_pos) != 2:
                continue

            distance = (
                abs(actor_pos[0] - resource_pos[0])
                + abs(actor_pos[1] - resource_pos[1])
            )
            if distance <= 1:
                return True

    return False


def is_set(state, *args):
    """True when the named status flag exists and has a truthy value."""
    if not args:
        return False

    flag = args[0]
    return bool(state.get(flag, False))