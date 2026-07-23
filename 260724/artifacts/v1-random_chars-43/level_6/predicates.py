from collections import deque


def _positive(value):
    """Return whether a raw-state counter represents a positive quantity."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return bool(value)


def _resource_key(target):
    """Map PDDL resource names to their raw-state world-object keys."""
    aliases = {
        "tpkhxk": "xcvkpr",
    }
    return aliases.get(target, target)


def _positions(state, key):
    """Return valid coordinate entries for a raw-state object as tuples."""
    result = set()
    for position in state.get(key, []):
        if isinstance(position, (list, tuple)) and len(position) == 2:
            result.add(tuple(position))
    return result


def achieved(state, *args):
    """True when the requested achievement flag has been earned."""
    if not args:
        return False
    flag = args[0]
    return _positive(state.get(flag, 0))


def inventory_at_least_one(state, *args):
    """True when at least one unit of the requested resource is held."""
    if not args:
        return False
    target = args[0]
    return _positive(state.get("inv_" + str(target), 0))


def placed(state, *args):
    """True when the requested resource has been placed by the player."""
    if not args:
        return False
    target = args[0]
    return _positive(state.get("ach_place_" + str(target), 0))


def reachable(state, *args):
    """
    True when the actor can walk to a traversable cell adjacent to the target.

    tpkhxk is represented by xcvkpr in the low-level world.
    """
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, str(who))
    target_positions = _positions(state, _resource_key(str(target)))

    if not actor_positions or not target_positions:
        return False

    start = next(iter(actor_positions))
    traversable = _positions(state, "pmzjpl")
    traversable.add(start)

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def adjacent_to_target(position):
        x, y = position
        return any(
            (x + dx, y + dy) in target_positions
            for dx, dy in directions
        )

    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()
        if adjacent_to_target(current):
            return True

        x, y = current
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in traversable and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """True when the actor is facing a target resource in an adjacent cell."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, str(who))
    target_positions = _positions(state, _resource_key(str(target)))

    if not actor_positions or not target_positions:
        return False

    facing = state.get(str(who) + "_facing")
    if facing is None and str(who) == "player":
        facing = state.get("player_facing")

    if not isinstance(facing, (list, tuple)) or len(facing) != 2:
        return False

    x, y = next(iter(actor_positions))
    target_cell = (x + facing[0], y + facing[1])
    return target_cell in target_positions