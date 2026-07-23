from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)
    new_state["step_count"] = state.get("step_count", 0) + 1

    if not state.get("player"):
        return new_state

    x, y = state["player"][0]

    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    def spatial_items(s):
        for key, value in s.items():
            if key == "player" or not isinstance(value, list):
                continue
            if all(
                isinstance(p, (list, tuple))
                and len(p) == 2
                and all(isinstance(v, (int, float)) for v in p)
                for p in value
            ):
                yield key, value

    def key_at(pos):
        p = list(pos)
        return [
            key
            for key, positions in spatial_items(new_state)
            if p in positions
        ]

    def remove_position(key, pos):
        p = list(pos)
        if p in new_state.get(key, []):
            new_state[key].remove(p)

    def add_position(key, pos):
        p = list(pos)
        new_state.setdefault(key, [])
        if p not in new_state[key]:
            new_state[key].append(p)
            new_state[key].sort(key=lambda point: (point[0], point[1]))

    def matching_key(pos, suffix):
        for key in key_at(pos):
            if key.endswith(suffix):
                return key
        return None

    def map_bounds():
        points = [
            p
            for _, positions in spatial_items(state)
            for p in positions
        ]
        if not points:
            return None
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return min(xs), max(xs), min(ys), max(ys)

    def in_bounds(pos):
        bounds = map_bounds()
        if bounds is None:
            return True
        min_x, max_x, min_y, max_y = bounds
        return (
            min_x <= pos[0] <= max_x
            and min_y <= pos[1] <= max_y
        )

    def is_walkable(pos):
        if not in_bounds(pos):
            return False
        occupants = key_at(pos)
        return any(
            key.endswith(("grass", "sand", "path", "floor"))
            for key in occupants
        )

    def front_position():
        facing = new_state.get("player_facing", [0, 1])
        return [x + facing[0], y + facing[1]]

    def station_nearby(suffix):
        for key, positions in spatial_items(new_state):
            if not key.endswith(suffix):
                continue
            for px, py in positions:
                if max(abs(px - x), abs(py - y)) <= 1:
                    return True
        return False

    # Movement changes facing even when an obstacle prevents displacement.
    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        destination = [x + dx, y + dy]
        if is_walkable(destination):
            new_state["player"] = [destination]
        return new_state

    if action == "sleep":
        new_state["player_sleeping"] = True
        return new_state

    if action == "do":
        target = front_position()

        # Trees can be harvested by hand.
        tree_key = matching_key(target, "tree")
        if tree_key is not None:
            remove_position(tree_key, target)
            add_position("grass", target)
            new_state["inv_wood"] = new_state.get("inv_wood", 0) + 1
            new_state["ach_collect_wood"] = (
                new_state.get("ach_collect_wood", 0) + 1
            )
            return new_state

        # Generic mining rules for mineral tiles.
        mining_rules = (
            ("diamond", "iron_pickaxe"),
            ("iron", "stone_pickaxe"),
            ("coal", "stone_pickaxe"),
            ("stone", "wood_pickaxe"),
        )
        for resource, required_tool in mining_rules:
            resource_key = matching_key(target, resource)
            if resource_key is None:
                continue

            tool_order = {
                "wood_pickaxe": 1,
                "stone_pickaxe": 2,
                "iron_pickaxe": 3,
            }
            required_level = tool_order[required_tool]
            has_tool = any(
                new_state.get("inv_" + tool, 0) > 0
                and level >= required_level
                for tool, level in tool_order.items()
            )
            if has_tool:
                remove_position(resource_key, target)
                add_position("path", target)
                new_state["inv_" + resource] = (
                    new_state.get("inv_" + resource, 0) + 1
                )
            return new_state

        return new_state

    # Placement occurs on the tile in front of the player.
    if action.startswith("place_"):
        item = action[len("place_"):]
        target = front_position()

        placement_costs = {
            "stone": ("stone", 1),
            "table": ("wood", 2),
            "furnace": ("stone", 4),
            "plant": ("sapling", 1),
        }

        if item not in placement_costs or not in_bounds(target):
            return new_state

        resource, cost = placement_costs[item]
        inventory_key = "inv_" + resource
        if new_state.get(inventory_key, 0) < cost:
            return new_state

        occupants = key_at(target)
        valid_ground = [
            key
            for key in occupants
            if key.endswith(("grass", "sand", "path", "floor"))
        ]
        if not valid_ground:
            return new_state

        for key in valid_ground:
            remove_position(key, target)

        add_position(item, target)
        new_state[inventory_key] -= cost
        achievement_key = "ach_place_" + item
        new_state[achievement_key] = new_state.get(achievement_key, 0) + 1
        return new_state

    if action.startswith("make_"):
        product = action[len("make_"):]

        recipes = {
            "wood_pickaxe": {"wood": 1},
            "stone_pickaxe": {"wood": 1, "stone": 1},
            "iron_pickaxe": {"wood": 1, "coal": 1, "iron": 1},
            "wood_sword": {"wood": 1},
            "stone_sword": {"wood": 1, "stone": 1},
            "iron_sword": {"wood": 1, "coal": 1, "iron": 1},
        }

        recipe = recipes.get(product)
        if recipe is None or not station_nearby("table"):
            return new_state

        if product.startswith("iron_") and not station_nearby("furnace"):
            return new_state

        if not all(
            new_state.get("inv_" + resource, 0) >= amount
            for resource, amount in recipe.items()
        ):
            return new_state

        for resource, amount in recipe.items():
            new_state["inv_" + resource] -= amount
        new_state["inv_" + product] = (
            new_state.get("inv_" + product, 0) + 1
        )
        return new_state

    # noop and unsuccessful/unknown actions only consume a step.
    return new_state