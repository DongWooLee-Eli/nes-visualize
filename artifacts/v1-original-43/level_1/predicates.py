from collections import deque


def _positions(state, name):
    """Return valid coordinate pairs associated with an object/resource name."""
    value = state.get(name, [])
    if not isinstance(value, list):
        return []

    return [
        (position[0], position[1])
        for position in value
        if (
            isinstance(position, (list, tuple))
            and len(position) == 2
            and all(isinstance(v, (int, float)) for v in position)
        )
    ]


def _matching_positions(state, name):
    """Return positions for an exact key or keys ending in the given name."""
    positions = []
    for key in state:
        if key == name or key.endswith(name):
            positions.extend(_positions(state, key))
    return positions


def _actor_position(state, actor):
    positions = _matching_positions(state, actor)
    return positions[0] if positions else None


def _is_ground_at(state, position):
    ground_suffixes = ("grass", "sand", "path", "floor")
    for key in state:
        if key.endswith(ground_suffixes) and position in _positions(state, key):
            return True
    return False


def ach_collect_wood(state, *args):
    """True once wood collection is evidenced by an achievement or world state."""
    if bool(state.get("ach_collect_wood", False)):
        return True

    if state.get("inv_wood", 0) > 0:
        return True

    # A placed table proves that at least two pieces of wood were collected,
    # even if the inventory was subsequently consumed.
    return bool(_matching_positions(state, "table")) or bool(
        state.get("ach_place_table", False)
    )


def ach_place_table(state, *args):
    """True when the table-placement achievement is set or a table exists."""
    return bool(state.get("ach_place_table", False)) or bool(
        _matching_positions(state, "table")
    )


def available(state, *args):
    """True when the requested resource has at least one remaining instance."""
    if not args:
        return False

    target = args[0]
    return bool(_matching_positions(state, target))


def can_place_table(state, *args):
    """True when the actor exists and the tile in front permits placement."""
    if not args:
        return False

    actor = args[0]
    actor_position = _actor_position(state, actor)
    if actor_position is None:
        return False

    facing = state.get("player_facing", [0, 1])
    if (
        not isinstance(facing, (list, tuple))
        or len(facing) != 2
        or not all(isinstance(v, (int, float)) for v in facing)
    ):
        return False

    target_position = (
        actor_position[0] + facing[0],
        actor_position[1] + facing[1],
    )
    return _is_ground_at(state, target_position)


def close_to(state, *args):
    """True when the actor is on or cardinally adjacent to the resource."""
    if len(args) < 2:
        return False

    actor, target = args[0], args[1]
    actor_position = _actor_position(state, actor)
    target_positions = _matching_positions(state, target)

    if actor_position is None or not target_positions:
        return False

    ax, ay = actor_position
    return any(abs(tx - ax) + abs(ty - ay) <= 1 for tx, ty in target_positions)


def reachable(state, *args):
    """True when a walkable route reaches the target or a tile beside it."""
    if len(args) < 2:
        return False

    actor, target = args[0], args[1]
    start = _actor_position(state, actor)
    target_positions = set(_matching_positions(state, target))

    if start is None or not target_positions:
        return False

    if any(abs(tx - start[0]) + abs(ty - start[1]) <= 1
           for tx, ty in target_positions):
        return True

    walkable = set()
    all_positions = []

    for key in state:
        positions = _positions(state, key)
        all_positions.extend(positions)
        if key.endswith(("grass", "sand", "path", "floor")):
            walkable.update(positions)

    if not all_positions:
        return False

    min_x = min(x for x, _ in all_positions)
    max_x = max(x for x, _ in all_positions)
    min_y = min(y for _, y in all_positions)
    max_y = max(y for _, y in all_positions)

    goals = {
        (tx + dx, ty + dy)
        for tx, ty in target_positions
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))
        if (tx + dx, ty + dy) in walkable
    }

    if start in goals:
        return True

    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = (x + dx, y + dy)

            if neighbor in visited:
                continue
            if not (min_x <= neighbor[0] <= max_x
                    and min_y <= neighbor[1] <= max_y):
                continue
            if neighbor not in walkable:
                continue
            if neighbor in goals:
                return True

            visited.add(neighbor)
            queue.append(neighbor)

    return False