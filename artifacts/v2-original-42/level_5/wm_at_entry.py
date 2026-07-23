from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)
    new_state["step_count"] = state.get("step_count", 0) + 1

    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    def positions(key):
        return new_state.get(key, [])

    def contains(key, pos):
        return pos in positions(key)

    def remove_at(key, pos):
        if contains(key, pos):
            new_state[key] = [p for p in positions(key) if p != pos]

    def add_at(key, pos):
        if pos not in positions(key):
            new_state.setdefault(key, []).append(pos)
            new_state[key].sort(key=lambda p: (p[0], p[1]))

    def inventory(item):
        return new_state.get("inv_" + item, 0)

    def spend(cost):
        if any(inventory(item) < amount for item, amount in cost.items()):
            return False
        for item, amount in cost.items():
            new_state["inv_" + item] = inventory(item) - amount
        return True

    def increment_achievement(name):
        new_state[name] = new_state.get(name, 0) + 1

    def coord_keys_at(pos):
        result = []
        for key, value in new_state.items():
            if key == "player" or not isinstance(value, list):
                continue
            if value and all(
                isinstance(p, list) and len(p) == 2 for p in value
            ) and pos in value:
                result.append(key)
        return result

    def map_bounds():
        coords = []
        for key, value in new_state.items():
            if key == "player" or not isinstance(value, list):
                continue
            for p in value:
                if (
                    isinstance(p, list)
                    and len(p) == 2
                    and all(isinstance(v, int) for v in p)
                ):
                    coords.append(p)
        if not coords:
            return None
        return (
            min(p[0] for p in coords),
            max(p[0] for p in coords),
            min(p[1] for p in coords),
            max(p[1] for p in coords),
        )

    def in_bounds(pos):
        bounds = map_bounds()
        if bounds is None:
            return True
        min_x, max_x, min_y, max_y = bounds
        return min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y

    def is_walkable(pos):
        if not in_bounds(pos):
            return False

        keys = coord_keys_at(pos)
        if not keys:
            return False

        passable = any(
            key.endswith(("grass", "sand", "path", "floor"))
            for key in keys
        )
        blocking = any(
            key.endswith((
                "water", "tree", "stone", "coal", "iron", "diamond",
                "table", "furnace", "plant", "wall"
            ))
            or key.startswith(("closed_", "enemy", "zombie", "skeleton"))
            for key in keys
        )
        return passable and not blocking

    player = new_state.get("player", [[0, 0]])
    px, py = player[0] if player else [0, 0]

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        destination = [px + dx, py + dy]
        if is_walkable(destination):
            new_state["player"] = [destination]
        return new_state

    facing = new_state.get("player_facing", [0, 1])
    target = [px + facing[0], py + facing[1]]

    if action == "do":
        target_keys = coord_keys_at(target)

        # Trees can be harvested by hand.
        tree_key = next(
            (key for key in target_keys if key.endswith("tree")), None
        )
        if tree_key is not None:
            remove_at(tree_key, target)
            add_at("grass", target)
            new_state["inv_wood"] = inventory("wood") + 1
            increment_achievement("ach_collect_wood")
            return new_state

        # Water interaction replenishes drink/thirst where represented.
        if any(key.endswith("water") for key in target_keys):
            if "inv_drink" in new_state:
                new_state["inv_drink"] = min(
                    9, new_state.get("inv_drink", 0) + 1
                )
            if "player_thirst" in new_state:
                new_state["player_thirst"] = 0.0
            return new_state

        resource_key = next(
            (
                key for key in target_keys
                if key.endswith(("stone", "coal", "iron", "diamond"))
            ),
            None,
        )

        if resource_key is not None:
            resource = resource_key.rsplit("_", 1)[-1]
            tool_ok = False

            if resource in ("stone", "coal"):
                tool_ok = any(
                    inventory(tool) > 0
                    for tool in (
                        "wood_pickaxe", "stone_pickaxe", "iron_pickaxe"
                    )
                )
            elif resource == "iron":
                tool_ok = any(
                    inventory(tool) > 0
                    for tool in ("stone_pickaxe", "iron_pickaxe")
                )
            elif resource == "diamond":
                tool_ok = inventory("iron_pickaxe") > 0

            if tool_ok:
                remove_at(resource_key, target)
                add_at("path", target)
                new_state["inv_" + resource] = inventory(resource) + 1
                increment_achievement("ach_collect_" + resource)

        return new_state

    placement = {
        "place_stone": ("stone", {"stone": 1}),
        "place_table": ("table", {"wood": 2}),
        "place_furnace": ("furnace", {"stone": 4}),
        "place_plant": ("plant", {"sapling": 1}),
    }

    if action in placement:
        entity, cost = placement[action]
        if is_walkable(target) and spend(cost):
            # Placed objects replace the walkable terrain at their location.
            for terrain_key in list(coord_keys_at(target)):
                if terrain_key.endswith(("grass", "sand", "path", "floor")):
                    remove_at(terrain_key, target)
            add_at(entity, target)
            increment_achievement("ach_place_" + entity)
        return new_state

    if action.startswith("make_"):
        item = action[len("make_"):]

        recipes = {
            "wood_pickaxe": {"wood": 1},
            "stone_pickaxe": {"wood": 1, "stone": 1},
            "iron_pickaxe": {"wood": 1, "coal": 1, "iron": 1},
            "wood_sword": {"wood": 1},
            "stone_sword": {"wood": 1, "stone": 1},
            "iron_sword": {"wood": 1, "coal": 1, "iron": 1},
        }

        recipe = recipes.get(item)
        if recipe is None:
            return new_state

        adjacent = [
            [px - 1, py], [px + 1, py],
            [px, py - 1], [px, py + 1],
        ]
        near_table = any(
            any(key.endswith("table") for key in coord_keys_at(pos))
            for pos in adjacent
        )
        near_furnace = any(
            any(key.endswith("furnace") for key in coord_keys_at(pos))
            for pos in adjacent
        )

        # All tools require a table; iron equipment also requires a furnace.
        can_craft = near_table
        if item.startswith("iron_"):
            can_craft = can_craft and near_furnace

        if can_craft and spend(recipe):
            inv_key = "inv_" + item
            new_state[inv_key] = new_state.get(inv_key, 0) + 1
            increment_achievement("ach_make_" + item)

        return new_state

    # noop, failed sleep, and unsupported actions only advance time.
    return new_state