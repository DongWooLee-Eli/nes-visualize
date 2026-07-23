def _positions(state, key):
    """Return valid (x, y) positions stored under a raw-state key."""
    value = state.get(key, [])
    if not isinstance(value, (list, tuple)):
        return set()

    result = set()
    for position in value:
        if isinstance(position, (list, tuple)) and len(position) == 2:
            x, y = position
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                result.add((x, y))
    return result


def _cell_position(cell):
    """Convert a cell argument into an (x, y) tuple when possible."""
    if isinstance(cell, (list, tuple)) and len(cell) == 2:
        x, y = cell
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return (x, y)

    # Support common symbolic cell forms such as "cell_4_3".
    if isinstance(cell, str):
        parts = cell.replace("(", "_").replace(")", "_").replace(",", "_").split("_")
        numbers = []
        for part in parts:
            try:
                numbers.append(int(part))
            except (TypeError, ValueError):
                pass
        if len(numbers) >= 2:
            return (numbers[-2], numbers[-1])

    return None


def _is_walkable(state, position):
    """True when position occurs in at least one spatial world layer."""
    if position is None:
        return False

    for key in state:
        if key == "player" or key.startswith("inv_"):
            continue
        if position in _positions(state, key):
            return True
    return False


def adjacent_to(state, *args):
    """True when an actor faces an adjacent occurrence of a resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = _positions(state, who)
    resource_positions = _positions(state, what)
    if not actor_positions or not resource_positions:
        return False

    facing_key = f"{who}_facing"
    facing = state.get(facing_key)
    if facing is None and who == "player":
        facing = state.get("player_facing")

    # Collection in the low-level model acts on the cell being faced.
    if isinstance(facing, (list, tuple)) and len(facing) == 2:
        dx, dy = facing
        if isinstance(dx, (int, float)) and isinstance(dy, (int, float)):
            return any((x + dx, y + dy) in resource_positions
                       for x, y in actor_positions)

    # Fall back to ordinary cardinal adjacency if facing is unavailable.
    return any(
        (x + dx, y + dy) in resource_positions
        for x, y in actor_positions
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))
    )


def at(state, *args):
    """True when an actor occupies the specified cell."""
    if len(args) < 2:
        return False

    who, where = args[0], args[1]
    position = _cell_position(where)
    return position is not None and position in _positions(state, who)


def can_move_down(state, *args):
    """True when `to` is the walkable cell directly below `from`."""
    if len(args) < 2:
        return False

    source = _cell_position(args[0])
    destination = _cell_position(args[1])
    return (
        source is not None
        and destination == (source[0], source[1] + 1)
        and _is_walkable(state, destination)
    )


def can_move_left(state, *args):
    """True when `to` is the walkable cell directly left of `from`."""
    if len(args) < 2:
        return False

    source = _cell_position(args[0])
    destination = _cell_position(args[1])
    return (
        source is not None
        and destination == (source[0] - 1, source[1])
        and _is_walkable(state, destination)
    )


def can_move_right(state, *args):
    """True when `to` is the walkable cell directly right of `from`."""
    if len(args) < 2:
        return False

    source = _cell_position(args[0])
    destination = _cell_position(args[1])
    return (
        source is not None
        and destination == (source[0] + 1, source[1])
        and _is_walkable(state, destination)
    )


def can_move_up(state, *args):
    """True when `to` is the walkable cell directly above `from`."""
    if len(args) < 2:
        return False

    source = _cell_position(args[0])
    destination = _cell_position(args[1])
    return (
        source is not None
        and destination == (source[0], source[1] - 1)
        and _is_walkable(state, destination)
    )