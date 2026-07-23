from collections import deque


def _positions(state, key):
    """Return valid coordinate tuples stored under a raw-state key."""
    value = state.get(key, [])
    if not isinstance(value, list):
        return set()

    return {
        (point[0], point[1])
        for point in value
        if isinstance(point, (list, tuple))
        and len(point) == 2
        and all(isinstance(component, (int, float)) for component in point)
    }


def close_to(state, *args):
    """True when the actor is cardinally adjacent to the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = _positions(state, who)
    target_positions = _positions(state, target)

    return any(
        abs(ax - tx) + abs(ay - ty) == 1
        for ax, ay in actor_positions
        for tx, ty in target_positions
    )


def is_set(state, *args):
    """True when the named status flag has a truthy raw-state value."""
    if not args:
        return False

    flag = args[0]
    return bool(state.get(flag, False))


def reachable(state, *args):
    """
    True when the actor can reach a walkable tile cardinally adjacent to
    the target resource.
    """
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    starts = _positions(state, who)
    targets = _positions(state, target)

    if not starts or not targets:
        return False

    # Interaction is possible from any cardinally adjacent position.
    goals = {
        (tx + dx, ty + dy)
        for tx, ty in targets
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
    }

    if starts & goals:
        return True

    walkable_suffixes = ("grass", "sand", "path", "floor")
    walkable = set(starts)

    for key in state:
        if isinstance(key, str) and key.endswith(walkable_suffixes):
            walkable.update(_positions(state, key))

    valid_goals = goals & walkable
    if not valid_goals:
        return False

    frontier = deque(starts)
    visited = set(starts)

    while frontier:
        x, y = frontier.popleft()

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = (x + dx, y + dy)

            if neighbor in valid_goals:
                return True

            if neighbor in walkable and neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)

    return False