from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)
    new_state["step_count"] = state.get("step_count", 0) + 1

    if not state.get("player"):
        return new_state

    position = state["player"][0]
    x, y = position
    facing = state.get("player_facing", [0, 1])

    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    def coordinates(key):
        value = new_state.get(key, [])
        if not isinstance(value, list):
            return set()
        return {
            tuple(item)
            for item in value
            if isinstance(item, (list, tuple))
            and len(item) == 2
            and all(isinstance(v, (int, float)) for v in item)
        }

    def add_tile(key, pos):
        tile = list(pos)
        new_state.setdefault(key, [])
        if tile not in new_state[key]:
            new_state[key].append(tile)

    def remove_tile(key, pos):
        tile = list(pos)
        if tile in new_state.get(key, []):
            new_state[key].remove(tile)
            return True
        return False

    def tile_key_at(pos):
        ignored = {"player", "player_facing"}
        for key in new_state:
            if key in ignored or key.startswith("inv_"):
                continue
            if tuple(pos) in coordinates(key):
                return key
        return None

    def occupied_by_blocker(pos):
        passable_suffixes = ("grass", "sand", "path", "floor")
        for key in new_state:
            if key == "player" or key.startswith("inv_"):
                continue
            if tuple(pos) not in coordinates(key):
                continue
            if not key.endswith(passable_suffixes):
                return True
        return False

    def map_bounds():
        points = []
        for key in new_state:
            if key == "player" or key.startswith("inv_"):
                continue
            points.extend(coordinates(key))
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
        return min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y

    def has_nearby(suffix):
        for key in new_state:
            if not key.endswith(suffix):
                continue
            for px, py in coordinates(key):
                if max(abs(px - x), abs(py - y)) <= 1:
                    return True
        return False

    # Movement changes facing even when the destination is blocked.
    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        destination = (x + dx, y + dy)
        if in_bounds(destination) and not occupied_by_blocker(destination):
            new_state["player"] = [[destination[0], destination[1]]]
        return new_state

    if action == "sleep":
        new_state["player_sleeping"] = True
        return new_state

    if action == "noop":
        return new_state

    target = (x + facing[0], y + facing[1])

    if action == "do":
        target_key = tile_key_at(target)
        if target_key is None:
            return new_state

        # Trees can be collected without a tool.
        if target_key.endswith("tree"):
            remove_tile(target_key, target)
            add_tile("grass", target)
            new_state["inv_wood"] = new_state.get("inv_wood", 0) + 1
            return new_state

        # Plants may mature into trees when interacted with.
        if target_key.endswith("plant"):
            remove_tile(target_key, target)
            add_tile("tree", target)
            return new_state

        # Mining progression.
        mining_requirements = {
            "stone": "inv_wood_pickaxe",
            "coal": "inv_wood_pickaxe",
            "iron": "inv_stone_pickaxe",
            "diamond": "inv_iron_pickaxe",
        }
        for resource, required_tool in mining_requirements.items():
            if target_key.endswith(resource):
                if new_state.get(required_tool, 0) > 0:
                    remove_tile(target_key, target)
                    add_tile("path", target)
                    inventory_key = "inv_" + resource
                    new_state[inventory_key] = new_state.get(inventory_key, 0) + 1
                return new_state

        return new_state

    # Placement occurs on the tile in front of the player.
    if action.startswith("place_"):
        item = action[len("place_"):]
        costs = {
            "stone": ("inv_stone", 1),
            "table": ("inv_wood", 2),
            "furnace": ("inv_stone", 4),
            "plant": ("inv_sapling", 1),
        }
        cost = costs.get(item)
        if cost is None or not in_bounds(target) or occupied_by_blocker(target):
            return new_state

        inventory_key, amount = cost
        if new_state.get(inventory_key, 0) < amount:
            return new_state

        # Replace passable ground with the placed object.
        for key in list(new_state):
            if key.endswith(("grass", "sand", "path", "floor")):
                remove_tile(key, target)

        new_state[inventory_key] -= amount
        add_tile(item, target)
        return new_state

    # Crafting requires a nearby table. Iron equipment additionally requires
    # a nearby furnace.
    if action.startswith("make_"):
        item = action[len("make_"):]
        recipes = {
            "wood_pickaxe": {"inv_wood": 1},
            "stone_pickaxe": {"inv_wood": 1, "inv_stone": 1},
            "iron_pickaxe": {"inv_wood": 1, "inv_coal": 1, "inv_iron": 1},
            "wood_sword": {"inv_wood": 1},
            "stone_sword": {"inv_wood": 1, "inv_stone": 1},
            "iron_sword": {"inv_wood": 1, "inv_coal": 1, "inv_iron": 1},
        }
        recipe = recipes.get(item)
        if recipe is None or not has_nearby("table"):
            return new_state
        if item.startswith("iron_") and not has_nearby("furnace"):
            return new_state
        if any(new_state.get(key, 0) < amount
               for key, amount in recipe.items()):
            return new_state

        for key, amount in recipe.items():
            new_state[key] -= amount
        result_key = "inv_" + item
        new_state[result_key] = new_state.get(result_key, 0) + 1
        return new_state

    return new_state