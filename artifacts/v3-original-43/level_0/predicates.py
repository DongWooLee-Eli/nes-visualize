def wood_reachable(state, *args):
    """True when the specified actor can reach a cell adjacent to the wood source."""
    if len(args) < 2:
        return False

    who, source = args[0], args[1]
    actor_positions = state.get(who, []) or []
    source_positions = state.get(source, []) or []

    if not actor_positions or not source_positions:
        return False

    def valid_positions(value):
        return (
            isinstance(value, list)
            and all(
                isinstance(pos, (list, tuple))
                and len(pos) == 2
                and all(isinstance(v, (int, float)) for v in pos)
                for pos in value
            )
        )

    layers = {
        key: {tuple(pos) for pos in value}
        for key, value in state.items()
        if key != who
        and not key.startswith("inv_")
        and valid_positions(value)
        and value
    }

    known_cells = set().union(*layers.values()) if layers else set()
    targets = {tuple(pos) for pos in source_positions}

    def is_ground(key):
        return (
            key.endswith("grass")
            or key.endswith("sand")
            or key.endswith("path")
            or key.endswith("floor")
        )

    def is_walkable(pos):
        keys = [key for key, positions in layers.items() if pos in positions]
        if not keys or not any(is_ground(key) for key in keys):
            return False

        blocked_suffixes = (
            "water", "tree", "stone", "coal", "iron", "diamond",
            "table", "furnace", "plant", "door"
        )
        return not any(
            not is_ground(key)
            and (key.endswith(blocked_suffixes) or key.startswith("closed_"))
            for key in keys
        )

    start = tuple(actor_positions[0])
    frontier = [start]
    visited = {start}

    while frontier:
        x, y = frontier.pop(0)
        neighbors = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

        if any(pos in targets for pos in neighbors):
            return True

        for pos in neighbors:
            if pos not in visited and pos in known_cells and is_walkable(pos):
                visited.add(pos)
                frontier.append(pos)

    return False