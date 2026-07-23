def adjacent_to(state, *args):
    """True when the actor is orthogonally adjacent to the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]

    def get_positions(entity):
        if isinstance(entity, str):
            value = state.get(entity, [])
        else:
            value = entity

        if (
            isinstance(value, (list, tuple))
            and len(value) == 2
            and all(isinstance(v, (int, float)) for v in value)
        ):
            return {(value[0], value[1])}

        if not isinstance(value, (list, tuple)):
            return set()

        return {
            (position[0], position[1])
            for position in value
            if (
                isinstance(position, (list, tuple))
                and len(position) == 2
                and all(isinstance(v, (int, float)) for v in position)
            )
        }

    actor_positions = get_positions(who)
    resource_positions = get_positions(what)

    return any(
        abs(actor_x - resource_x) + abs(actor_y - resource_y) == 1
        for actor_x, actor_y in actor_positions
        for resource_x, resource_y in resource_positions
    )