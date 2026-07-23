from collections import deque


def achieved(state, *args):
    """True when the requested achievement flag is set or its collection is evident."""
    if not args:
        return False

    flag = args[0]

    # Prefer the explicit achievement value when the environment provides it.
    if bool(state.get(flag, 0)):
        return True

    # Collection achievements can also be inferred from the corresponding
    # inventory, which is updated by the low-level transition model.
    prefix = "ach_collect_"
    if isinstance(flag, str) and flag.startswith(prefix):
        resource = flag[len(prefix):]
        return state.get("inv_" + resource, 0) > 0

    return False


def reachable(state, *args):
    """True when the actor can reach a ground cell adjacent to the resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_locations = state.get(who, [])
    target_locations = state.get(target, [])

    if not actor_locations or not target_locations:
        return False

    try:
        start = tuple(actor_locations[0])
        resources = {tuple(position) for position in target_locations}
        ground = {tuple(position) for position in state.get("pmzjpl", [])}
    except (TypeError, ValueError):
        return False

    if len(start) != 2 or not resources:
        return False

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def adjacent_to_resource(position):
        x, y = position
        return any((x + dx, y + dy) in resources for dx, dy in directions)

    if adjacent_to_resource(start):
        return True

    # Movement is possible only through pmzjpl cells.
    traversable = ground | {start}
    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in visited or neighbor not in traversable:
                continue

            if adjacent_to_resource(neighbor):
                return True

            visited.add(neighbor)
            queue.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """True when the actor is directly adjacent to the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_locations = state.get(who, [])
    target_locations = state.get(target, [])

    if not actor_locations or not target_locations:
        return False

    try:
        actor_positions = {tuple(position) for position in actor_locations}
        target_positions = {tuple(position) for position in target_locations}
    except (TypeError, ValueError):
        return False

    return any(
        abs(actor_x - target_x) + abs(actor_y - target_y) == 1
        for actor_x, actor_y in actor_positions
        for target_x, target_y in target_positions
    )