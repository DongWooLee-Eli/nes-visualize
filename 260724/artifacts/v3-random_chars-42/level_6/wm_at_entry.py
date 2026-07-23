from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)

    # Every observed action consumes one step, even when it has no other effect.
    new_state["step_count"] = state.get("step_count", 0) + 1

    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]

        player = state.get("player", [])
        if not player:
            return new_state

        x, y = player[0]
        current = (x, y)
        destination = (x + dx, y + dy)

        coordinate_fields = {}
        all_coordinates = []

        for key, value in state.items():
            if key == "player" or not isinstance(value, list):
                continue

            positions = set()
            for position in value:
                if (
                    isinstance(position, (list, tuple))
                    and len(position) == 2
                    and all(isinstance(v, int) for v in position)
                ):
                    pos = tuple(position)
                    positions.add(pos)
                    all_coordinates.append(pos)

            if positions:
                coordinate_fields[key] = positions

        if all_coordinates:
            min_x = min(px for px, _ in all_coordinates)
            max_x = max(px for px, _ in all_coordinates)
            min_y = min(py for _, py in all_coordinates)
            max_y = max(py for _, py in all_coordinates)
            in_bounds = (
                min_x <= destination[0] <= max_x
                and min_y <= destination[1] <= max_y
            )
        else:
            in_bounds = destination[0] >= 0 and destination[1] >= 0

        blocked = False

        # Explicitly named blockers remain impassable.
        for key, positions in coordinate_fields.items():
            key_lower = str(key).lower()
            is_blocker = (
                key_lower.startswith(("wall", "obstacle", "blocked", "closed_"))
                or key_lower.endswith(("_wall", "_obstacle", "_barrier"))
                or key_lower in {"walls", "obstacles", "blocked", "barriers"}
            )
            if is_blocker and destination in positions:
                blocked = True
                break

        # Opaque coordinate fields describe terrain/entity layers. A player may
        # move through the layer containing its current tile, but not directly
        # onto a tile belonging only to another layer.
        if not blocked and coordinate_fields:
            current_layers = {
                key for key, positions in coordinate_fields.items()
                if current in positions
            }
            destination_layers = {
                key for key, positions in coordinate_fields.items()
                if destination in positions
            }

            if current_layers and destination_layers.isdisjoint(current_layers):
                blocked = True

        if in_bounds and not blocked:
            new_state["player"] = [[destination[0], destination[1]]]

        return new_state

    if action.startswith("place_"):
        entity = action[len("place_"):]
        inventory_key = "inv_" + entity
        count = state.get(inventory_key, 0)

        player = state.get("player", [])
        facing = state.get("player_facing", [0, 0])

        if count > 0 and player and len(facing) == 2:
            x, y = player[0]
            target = [x + facing[0], y + facing[1]]

            occupied = target in new_state.get(entity, [])
            if not occupied:
                new_state[inventory_key] = count - 1
                new_state.setdefault(entity, []).append(target)

        return new_state

    # No successful do, sleep, or make transition was observed. They therefore
    # conservatively leave the state unchanged apart from consuming a step.
    return new_state