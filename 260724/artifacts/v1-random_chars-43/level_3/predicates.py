from collections import deque


def _positions(state, key):
    """Return valid grid positions stored under key as a set of tuples."""
    result = set()
    for position in state.get(key, []) or []:
        if isinstance(position, (list, tuple)) and len(position) == 2:
            result.add(tuple(position))
    return result


def _resource_key(target):
    """Map PDDL resource names to their corresponding raw-state map keys."""
    aliases = {
        "tpkhxk": "xcvkpr",  # Trees yield the tpkhxk resource.
    }
    return aliases.get(target, target)


def achieved(state, *args):
    """True when the requested achievement flag has been completed."""
    if not args:
        return False

    flag = args[0]

    # Prefer an explicit achievement value when the world model supplies one.
    if bool(state.get(flag, False)):
        return True

    # The low-level transition model records crafted products in inventory but
    # does not update achievement counters, so derive crafting achievements.
    make_prefix = "ach_make_"
    if isinstance(flag, str) and flag.startswith(make_prefix):
        product = flag[len(make_prefix):]
        return state.get("inv_" + product, 0) >= 1

    # Likewise, collection is observable from the corresponding inventory.
    collect_prefix = "ach_collect_"
    if isinstance(flag, str) and flag.startswith(collect_prefix):
        resource = flag[len(collect_prefix):]
        return state.get("inv_" + resource, 0) >= 1

    # Placement achievements are observable from objects on the map.
    place_prefix = "ach_place_"
    if isinstance(flag, str) and flag.startswith(place_prefix):
        placement = flag[len(place_prefix):]
        return bool(_positions(state, placement))

    return False


def inventory_at_least_one(state, *args):
    """True when at least one unit of the requested resource is held."""
    if not args:
        return False

    target = args[0]
    try:
        return state.get("inv_" + target, 0) >= 1
    except (TypeError, ValueError):
        return False


def placed(state, *args):
    """True when the requested placement exists somewhere in the world."""
    if not args:
        return False

    target = args[0]
    return bool(_positions(state, target))


def reachable(state, *args):
    """
    True when the actor can reach a traversable cell adjacent to the resource.

    Traversal follows the pmzjpl ground cells used by the low-level movement
    model. The resource tpkhxk is harvested from raw-state xcvkpr cells.
    """
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, who)
    resource_positions = _positions(state, _resource_key(target))

    if not actor_positions or not resource_positions:
        return False

    traversable = _positions(state, "pmzjpl")
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    # Cells from which the resource can be interacted with.
    approach_cells = {
        (rx + dx, ry + dy)
        for rx, ry in resource_positions
        for dx, dy in directions
        if (rx + dx, ry + dy) in traversable
    }

    if not approach_cells:
        return False

    queue = deque(position for position in actor_positions
                  if position in traversable)
    visited = set(queue)

    while queue:
        position = queue.popleft()
        if position in approach_cells:
            return True

        x, y = position
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in traversable and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """
    True when the requested resource is directly in front of the actor.

    This matches the low-level world's `do` interaction semantics.
    """
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, who)
    resource_positions = _positions(state, _resource_key(target))

    if not actor_positions or not resource_positions:
        return False

    facing = state.get("player_facing", [0, 1])
    if not isinstance(facing, (list, tuple)) or len(facing) != 2:
        return False

    try:
        dx, dy = facing
        return any(
            (x + dx, y + dy) in resource_positions
            for x, y in actor_positions
        )
    except (TypeError, ValueError):
        return False