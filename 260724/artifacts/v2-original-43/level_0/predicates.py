def achieved(state, *args):
    """True when the requested achievement has been completed."""
    if not args:
        return False

    result = args[0]
    value = state.get(result, 0)
    if bool(value):
        return True

    # The low-level model records collection through inventory changes but
    # does not directly update achievement flags.
    prefix = "ach_collect_"
    if isinstance(result, str) and result.startswith(prefix):
        resource = result[len(prefix):]
        return state.get("inv_" + resource, 0) > 0

    return False


def adjacent_to(state, *args):
    """True when an actor is orthogonally adjacent to a target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not isinstance(actor_positions, (list, tuple)):
        return False
    if not isinstance(target_positions, (list, tuple)):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) != 2:
            continue

        for target_pos in target_positions:
            if not isinstance(target_pos, (list, tuple)) or len(target_pos) != 2:
                continue

            try:
                distance = (
                    abs(actor_pos[0] - target_pos[0])
                    + abs(actor_pos[1] - target_pos[1])
                )
            except TypeError:
                continue

            if distance == 1:
                return True

    return False