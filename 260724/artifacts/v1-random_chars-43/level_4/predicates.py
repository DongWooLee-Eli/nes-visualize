from collections import deque


def achieved(state, *args):
    """True when the requested achievement is recorded or its result exists."""
    if not args:
        return False

    flag = args[0]

    if bool(state.get(flag, 0)):
        return True

    if flag.startswith("ach_collect_"):
        resource = flag[len("ach_collect_"):]
        return state.get("inv_" + resource, 0) >= 1

    if flag.startswith("ach_make_"):
        product = flag[len("ach_make_"):]
        return state.get("inv_" + product, 0) >= 1

    if flag.startswith("ach_place_"):
        placement = flag[len("ach_place_"):]
        return bool(state.get(placement, []))

    return False


def inventory_at_least_one(state, *args):
    """True when at least one unit of the specified resource is held."""
    if not args:
        return False

    target = args[0]
    try:
        return state.get("inv_" + target, 0) >= 1
    except TypeError:
        return False


def placed(state, *args):
    """True when at least one instance of the placement exists in the world."""
    if not args:
        return False

    target = args[0]
    return bool(state.get(target, []))


def reachable(state, *args):
    """True when the actor can reach a ground cell adjacent to the resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not actor_positions or not target_positions:
        return False

    try:
        start = tuple(actor_positions[0])
        targets = {tuple(position) for position in target_positions}
        traversable = {tuple(position) for position in state.get("pmzjpl", [])}
    except (TypeError, ValueError):
        return False

    if len(start) != 2:
        return False

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def adjacent_to_target(position):
        x, y = position
        return any((x + dx, y + dy) in targets for dx, dy in directions)

    if adjacent_to_target(start):
        return True

    traversable.add(start)
    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor not in traversable or neighbor in visited:
                continue

            if adjacent_to_target(neighbor):
                return True

            visited.add(neighbor)
            queue.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """True when the actor is standing next to the specified resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not actor_positions or not target_positions:
        return False

    try:
        actor_x, actor_y = actor_positions[0]
        targets = {tuple(position) for position in target_positions}
    except (TypeError, ValueError):
        return False

    return any(
        (actor_x + dx, actor_y + dy) in targets
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
    )