def _positions(state, key):
    """Return valid (x, y) positions for a spatial raw-state key."""
    value = state.get(key, [])
    if not isinstance(value, list):
        return set()
    return {
        tuple(position)
        for position in value
        if isinstance(position, (list, tuple)) and len(position) == 2
    }


def _matching_spatial_keys(state, object_name):
    """Find spatial keys corresponding to a PDDL object name."""
    if not isinstance(object_name, str):
        return []

    return [
        key
        for key, value in state.items()
        if isinstance(value, list)
        and (key == object_name or key.endswith(object_name))
    ]


def achieved(state, *args):
    """True when the requested achievement/status flag is set."""
    if not args:
        return False

    flag = args[0]
    return bool(state.get(flag, 0))


def adjacent_to(state, *args):
    """True when the actor is orthogonally adjacent to the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, who)
    if not actor_positions:
        return False

    target_positions = set()
    for key in _matching_spatial_keys(state, target):
        target_positions.update(_positions(state, key))

    return any(
        abs(actor_x - target_x) + abs(actor_y - target_y) == 1
        for actor_x, actor_y in actor_positions
        for target_x, target_y in target_positions
    )


def harvestable_wood(state, *args):
    """True when the specified wood resource has at least one tree remaining."""
    if not args:
        return False

    target = args[0]
    return any(
        bool(_positions(state, key))
        for key in _matching_spatial_keys(state, target)
    )


def placement_ready(state, *args):
    """True when the tile in front of the actor is valid for placement."""
    if not args:
        return False

    who = args[0]
    actor_positions = _positions(state, who)
    if not actor_positions:
        return False

    facing = state.get("player_facing", [0, 1])
    if not isinstance(facing, (list, tuple)) or len(facing) != 2:
        return False

    try:
        dx, dy = facing
        if abs(dx) + abs(dy) != 1:
            return False
    except (TypeError, ValueError):
        return False

    actor_x, actor_y = next(iter(actor_positions))
    target_position = (actor_x + dx, actor_y + dy)

    target_entities = []
    all_map_positions = set()

    for key, value in state.items():
        if key == who or not isinstance(value, list):
            continue

        positions = _positions(state, key)
        all_map_positions.update(positions)
        if target_position in positions:
            target_entities.append(key)

    if target_position not in all_map_positions:
        return False

    return bool(target_entities) and all(
        key.endswith(("grass", "sand", "path", "water"))
        for key in target_entities
    )


def wood_at_least_one(state, *args):
    """True when the actor's inventory contains at least one unit of wood."""
    return state.get("inv_wood", 0) >= 1


def wood_at_least_two(state, *args):
    """True when the actor's inventory contains at least two units of wood."""
    return state.get("inv_wood", 0) >= 2