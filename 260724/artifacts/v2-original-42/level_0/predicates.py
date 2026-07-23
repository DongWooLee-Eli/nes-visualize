def close_to(state, *args):
    """True when the actor is cardinally adjacent to the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not isinstance(actor_positions, list) or not isinstance(target_positions, list):
        return False

    for actor_pos in actor_positions:
        if not (
            isinstance(actor_pos, (list, tuple))
            and len(actor_pos) == 2
        ):
            continue

        for target_pos in target_positions:
            if not (
                isinstance(target_pos, (list, tuple))
                and len(target_pos) == 2
            ):
                continue

            if (
                abs(actor_pos[0] - target_pos[0])
                + abs(actor_pos[1] - target_pos[1])
                == 1
            ):
                return True

    return False