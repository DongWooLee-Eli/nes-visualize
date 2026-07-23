from collections import deque


def _positive(value):
    """Return whether a raw-state counter represents a positive quantity."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return bool(value)


def _resource_key(target):
    """Map a PDDL resource name to its corresponding world-state object key."""
    # Raw trees (xcvkpr) are the source of the abstract tpkhxk resource.
    if target == "tpkhxk":
        return "xcvkpr"
    return target


def achieved(state, flag):
    """True when the requested achievement has been completed."""
    if _positive(state.get(flag, 0)):
        return True

    if flag.startswith("ach_collect_"):
        resource = flag[len("ach_collect_"):]
        return _positive(state.get("inv_" + resource, 0))

    if flag.startswith("ach_make_"):
        product = flag[len("ach_make_"):]
        return _positive(state.get("inv_" + product, 0))

    if flag.startswith("ach_place_"):
        placement = flag[len("ach_place_"):]
        return bool(state.get(placement, []))

    return False


def inventory_at_least_one(state, target):
    """True when at least one unit of target is in the inventory."""
    return _positive(state.get("inv_" + target, 0))


def placed(state, target):
    """True when at least one instance of target is placed in the world."""
    return bool(state.get(target, []))


def reachable(state, who, target):
    """True when the actor can reach a ground cell adjacent to target."""
    if who not in state or not state.get(who):
        return False

    resource_positions = {
        tuple(position)
        for position in state.get(_resource_key(target), [])
        if isinstance(position, (list, tuple)) and len(position) == 2
    }
    if not resource_positions:
        return False

    start_data = state[who][0]
    if not isinstance(start_data, (list, tuple)) or len(start_data) != 2:
        return False
    start = tuple(start_data)

    ground = {
        tuple(position)
        for position in state.get("pmzjpl", [])
        if isinstance(position, (list, tuple)) and len(position) == 2
    }
    ground.add(start)

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()

        if any((x + dx, y + dy) in resource_positions
               for dx, dy in directions):
            return True

        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in ground and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def ready_to_collect(state, who, target):
    """True when the actor is facing an adjacent collectible target."""
    if who not in state or not state.get(who):
        return False

    position = state[who][0]
    facing = state.get(who + "_facing", state.get("player_facing", [0, 1]))

    if (
        not isinstance(position, (list, tuple))
        or len(position) != 2
        or not isinstance(facing, (list, tuple))
        or len(facing) != 2
    ):
        return False

    front = (position[0] + facing[0], position[1] + facing[1])
    resource_positions = {
        tuple(resource_position)
        for resource_position in state.get(_resource_key(target), [])
        if isinstance(resource_position, (list, tuple))
        and len(resource_position) == 2
    }

    return front in resource_positions