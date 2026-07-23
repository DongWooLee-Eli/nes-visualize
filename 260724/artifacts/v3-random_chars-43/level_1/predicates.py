def ach_place_zezroc(state, *args):
    """True when the zezroc placement achievement has been completed."""
    return bool(state.get("ach_place_zezroc", 0))


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

    def valid_position(position):
        return (
            isinstance(position, (list, tuple))
            and len(position) == 2
            and all(isinstance(value, (int, float)) for value in position)
        )

    actors = [position for position in actor_positions if valid_position(position)]
    resources = [position for position in resource_positions if valid_position(position)]

    return any(
        abs(actor[0] - resource[0]) + abs(actor[1] - resource[1]) == 1
        for actor in actors
        for resource in resources
    )