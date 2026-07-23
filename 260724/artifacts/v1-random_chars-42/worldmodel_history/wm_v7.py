from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)

    # Every observed action advances the environment by one step.
    new_state["step_count"] = state.get("step_count", 0) + 1

    player = state.get("player", [])
    if not player:
        return new_state

    x, y = player[0]

    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    harvest_drops = {
        "xcvkpr": "tpkhxk",
    }

    def coordinate_layers(s):
        """Return keys whose values look like lists of [x, y] positions."""
        layers = {}
        for key, value in s.items():
            if key == "player" or not isinstance(value, list):
                continue
            if all(
                isinstance(position, (list, tuple))
                and len(position) == 2
                and all(isinstance(v, int) for v in position)
                for position in value
            ):
                layers[key] = value
        return layers

    layers = coordinate_layers(state)

    # Layers without corresponding inventory items are terrain rather than
    # placeable entities. Harvestable layers are handled separately.
    terrain_keys = [
        key
        for key in layers
        if ("inv_" + key) not in state and key not in harvest_drops
    ]

    # Remember the terrain beneath the player for replacing harvested tiles.
    local_ground_keys = [
        key for key in terrain_keys if [x, y] in layers.get(key, [])
    ]

    all_positions = {
        tuple(position)
        for positions in layers.values()
        for position in positions
    }

    if all_positions:
        min_x = min(px for px, _ in all_positions)
        max_x = max(px for px, _ in all_positions)
        min_y = min(py for _, py in all_positions)
        max_y = max(py for _, py in all_positions)
    else:
        min_x = min_y = 0
        max_x = max_y = 0

    def in_bounds(position):
        px, py = position
        return min_x <= px <= max_x and min_y <= py <= max_y

    def is_ground(position):
        """All demonstrated terrain layers are traversable ground types."""
        p = list(position)
        return any(p in state.get(key, []) for key in terrain_keys)

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        target = (x + dx, y + dy)

        # Different terrain layers can represent different traversable ground
        # types, so movement is allowed onto any demonstrated terrain tile.
        if in_bounds(target) and (not terrain_keys or is_ground(target)):
            new_state["player"] = [[target[0], target[1]]]

    elif action == "do":
        dx, dy = state.get("player_facing", [0, 1])
        target = [x + dx, y + dy]

        for key, resource in harvest_drops.items():
            positions = state.get(key, [])
            if target not in positions:
                continue

            inventory_key = "inv_" + resource
            new_state[inventory_key] = state.get(inventory_key, 0) + 1
            new_state[key].remove(target)

            achievement_key = "ach_collect_" + resource
            new_state[achievement_key] = state.get(achievement_key, 0) + 1

            # Harvested tiles become the terrain type beneath the player.
            if local_ground_keys:
                ground_key = local_ground_keys[0]
                if target not in new_state.get(ground_key, []):
                    new_state.setdefault(ground_key, []).append(target)
                    new_state[ground_key].sort()
            break

    elif action.startswith("place_"):
        entity = action[len("place_"):]
        inventory_key = "inv_" + entity
        dx, dy = state.get("player_facing", [0, 1])
        target = [x + dx, y + dy]

        if (
            state.get(inventory_key, 0) > 0
            and in_bounds(tuple(target))
            and is_ground(tuple(target))
        ):
            new_state[inventory_key] -= 1

            for ground_key in terrain_keys:
                if target in new_state.get(ground_key, []):
                    new_state[ground_key].remove(target)
                    break

            if target not in new_state.setdefault(entity, []):
                new_state[entity].append(target)
                new_state[entity].sort()

    # Crafting, sleeping, noop, and unsupported actions have no demonstrated
    # effect beyond advancing step_count when their requirements are unmet.
    return new_state