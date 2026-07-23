def adjacent_to(state, *args):
    """True when the actor occupies a cell orthogonally adjacent to the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = state.get(who, [])
    resource_positions = state.get(what, [])

    if not isinstance(actor_positions, (list, tuple)):
        return False
    if not isinstance(resource_positions, (list, tuple)):
        return False

    valid_actor_positions = [
        position
        for position in actor_positions
        if isinstance(position, (list, tuple)) and len(position) == 2
    ]
    valid_resource_positions = [
        position
        for position in resource_positions
        if isinstance(position, (list, tuple)) and len(position) == 2
    ]

    return any(
        abs(actor[0] - resource[0]) + abs(actor[1] - resource[1]) == 1
        for actor in valid_actor_positions
        for resource in valid_resource_positions
    )