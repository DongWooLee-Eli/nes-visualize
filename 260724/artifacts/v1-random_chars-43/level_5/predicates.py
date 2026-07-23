def achieved(state, *args):
    """True when the specified achievement flag has been earned."""
    if not args:
        return False
    flag = args[0]
    return bool(state.get(flag, 0))


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
    """True when the specified resource has been placed by the player."""
    if not args:
        return False
    target = args[0]
    return bool(state.get("ach_place_" + target, 0))


def reachable(state, *args):
    """True when the actor can walk to a cell adjacent to the target."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    if not actor_positions:
        return False

    # Domain resource tpkhxk is represented by xcvkpr blocks in the world.
    world_key = "xcvkpr" if target == "tpkhxk" else target

    target_cells = {
        tuple(position)
        for position in state.get(world_key, [])
        if isinstance(position, (list, tuple)) and len(position) == 2
    }
    if not target_cells:
        return False

    try:
        start = tuple(actor_positions[0])
    except (TypeError, IndexError):
        return False
    if len(start) != 2:
        return False

    ground = {
        tuple(position)
        for position in state.get("pmzjpl", [])
        if isinstance(position, (list, tuple)) and len(position) == 2
    }
    ground.add(start)

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    interaction_cells = {
        (tx + dx, ty + dy)
        for tx, ty in target_cells
        for dx, dy in directions
        if (tx + dx, ty + dy) in ground
    }
    if not interaction_cells:
        return False

    frontier = [start]
    visited = {start}

    while frontier:
        current = frontier.pop()
        if current in interaction_cells:
            return True

        x, y = current
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in ground and neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)

    return False


def ready_to_collect(state, *args):
    """True when the specified target is directly in front of the actor."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    if not actor_positions:
        return False

    try:
        x, y = actor_positions[0]
    except (TypeError, ValueError, IndexError):
        return False

    facing = state.get(who + "_facing", state.get("player_facing", [0, 1]))
    if not isinstance(facing, (list, tuple)) or len(facing) != 2:
        return False

    world_key = "xcvkpr" if target == "tpkhxk" else target
    target_cells = {
        tuple(position)
        for position in state.get(world_key, [])
        if isinstance(position, (list, tuple)) and len(position) == 2
    }

    cell_in_front = (x + facing[0], y + facing[1])
    return cell_in_front in target_cells