from collections import deque


def _truthy(value):
    """Interpret common numeric, boolean, and collection state values."""
    if isinstance(value, str):
        return value.strip().lower() not in {"", "0", "false", "none", "no"}
    return bool(value)


def _positions(state, key):
    """Return the valid grid positions stored under a raw-state key."""
    result = set()
    for position in state.get(key, []):
        if isinstance(position, (list, tuple)) and len(position) == 2:
            result.add((position[0], position[1]))
    return result


def achieved(state, *args):
    """True when the requested achievement/status flag has been attained."""
    if not args:
        return False

    flag = str(args[0])
    candidates = [flag]

    if not flag.startswith("ach_"):
        candidates.append("ach_" + flag)
    if not flag.startswith("ach_collect_"):
        candidates.append("ach_collect_" + flag)

    for key in candidates:
        if key in state and _truthy(state[key]):
            return True

    # Collection achievements can also be inferred from current inventory.
    resource = flag
    for prefix in ("ach_collect_", "collect_"):
        if resource.startswith(prefix):
            resource = resource[len(prefix):]
            break

    return state.get("inv_" + resource, 0) > 0


def placed(state, *args):
    """True when the requested placement exists in the world."""
    if not args:
        return False

    target = str(args[0])
    if _positions(state, target):
        return True

    achievement_key = (
        target if target.startswith("ach_place_")
        else "ach_place_" + target
    )
    return _truthy(state.get(achievement_key, False))


def reachable(state, *args):
    """True when the player can reach a cell adjacent to the target resource."""
    if len(args) < 2:
        return False

    target = str(args[1])
    targets = _positions(state, target)
    players = _positions(state, "player")
    traversable = _positions(state, "pmzjpl")

    if not targets or not players:
        return False

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    goals = {
        (tx + dx, ty + dy)
        for tx, ty in targets
        for dx, dy in directions
        if (tx + dx, ty + dy) in traversable
    }

    start = next(iter(players))
    if start in goals:
        return True

    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in visited or neighbor not in traversable:
                continue
            if neighbor in goals:
                return True
            visited.add(neighbor)
            queue.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """True when the requested resource is directly in front of the player."""
    if len(args) < 2:
        return False

    target = str(args[1])
    players = _positions(state, "player")
    if not players:
        return False

    facing = state.get("player_facing", [0, 1])
    if not isinstance(facing, (list, tuple)) or len(facing) != 2:
        return False

    x, y = next(iter(players))
    front = (x + facing[0], y + facing[1])
    return front in _positions(state, target)