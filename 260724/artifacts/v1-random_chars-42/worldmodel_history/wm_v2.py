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

    def coordinate_layers(s):
        """Return keys whose values look like lists of [x, y] positions."""
        layers = {}
        for key, value in s.items():
            if key == "player" or not isinstance(value, list):
                continue
            if all(
                isinstance(p, (list, tuple))
                and len(p) == 2
                and all(isinstance(v, int) for v in p)
                for p in value
            ):
                layers[key] = value
        return layers

    layers = coordinate_layers(state)

    # A layer containing the player and lacking a corresponding inventory item
    # is treated as traversable ground.
    ground_keys = [
        key
        for key, positions in layers.items()
        if [x, y] in positions and ("inv_" + key) not in state
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
        p = list(position)
        return any(p in state.get(key, []) for key in ground_keys)

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        target = (x + dx, y + dy)

        # Movement is allowed only onto the traversable ground layer.
        if in_bounds(target) and (not ground_keys or is_ground(target)):
            new_state["player"] = [[target[0], target[1]]]

    elif action == "do":
        dx, dy = state.get("player_facing", [0, 1])
        target = [x + dx, y + dy]

        # Some world layers yield a differently named resource when harvested.
        harvest_drops = {
            "xcvkpr": "tpkhxk",
        }

        # Layers that may have similarly named inventory fields but represent
        # non-harvestable terrain.
        non_harvestable_layers = {
            "sgqeje",
        }

        for key, positions in layers.items():
            if target not in positions or key in non_harvestable_layers:
                continue

            resource = harvest_drops.get(key)
            if resource is None and ("inv_" + key) in state:
                resource = key

            if resource is None:
                continue

            inventory_key = "inv_" + resource
            new_state[inventory_key] = state.get(inventory_key, 0) + 1
            new_state[key].remove(target)

            # Record the first collection achievement for the resource.
            achievement_key = "ach_collect_" + resource
            new_state[achievement_key] = max(
                1, state.get(achievement_key, 0)
            )

            # Harvested tiles become the local ground type.
            if ground_keys:
                ground_key = ground_keys[0]
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

            for ground_key in ground_keys:
                if target in new_state.get(ground_key, []):
                    new_state[ground_key].remove(target)
                    break

            if target not in new_state.setdefault(entity, []):
                new_state[entity].append(target)
                new_state[entity].sort()

    # Crafting, sleeping, noop, and unsupported actions have no demonstrated
    # effect beyond advancing step_count when their requirements are unmet.
    return new_state