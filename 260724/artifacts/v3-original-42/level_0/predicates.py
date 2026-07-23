def close_to(state, *args):
    """True when the actor is within one grid cell of the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = state.get(who, []) or []
    resource_positions = state.get(what, []) or []

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) < 2:
            continue

        ax, ay = actor_pos[0], actor_pos[1]
        for resource_pos in resource_positions:
            if (
                isinstance(resource_pos, (list, tuple))
                and len(resource_pos) >= 2
                and max(
                    abs(resource_pos[0] - ax),
                    abs(resource_pos[1] - ay),
                ) <= 1
            ):
                return True

    return False