from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)
    new_state["step_count"] = state.get("step_count", 0) + 1

    if not state.get("player"):
        return new_state

    x, y = state["player"][0]
    facing = state.get("player_facing", [0, 1])
    directions = {
        "move_left": (-1, 0),
        "move_right": (1, 0),
        "move_up": (0, -1),
        "move_down": (0, 1),
    }

    def positions(key):
        value = new_state.get(key, [])
        if not isinstance(value, list):
            return set()
        return {
            tuple(pos) for pos in value
            if isinstance(pos, (list, tuple)) and len(pos) == 2
        }

    def entity_at(pos):
        found = []
        for key, value in new_state.items():
            if key == "player" or not isinstance(value, list):
                continue
            if pos in positions(key):
                found.append(key)
        return found

    def remove_at(key, pos):
        new_state[key] = [
            p for p in new_state.get(key, [])
            if not (isinstance(p, (list, tuple)) and tuple(p) == pos)
        ]

    def add_at(key, pos):
        new_state.setdefault(key, [])
        if list(pos) not in new_state[key]:
            new_state[key].append(list(pos))
            new_state[key].sort(key=lambda p: (p[0], p[1]))

    def replace_tile(pos, new_key):
        for key in list(new_state):
            if key == "player" or not isinstance(new_state.get(key), list):
                continue
            remove_at(key, pos)
        add_at(new_key, pos)

    def has_nearby(suffix):
        for key in new_state:
            if key.endswith(suffix):
                for px, py in positions(key):
                    if abs(px - x) <= 1 and abs(py - y) <= 1:
                        return True
        return False

    # Infer map bounds from all spatial layers.
    all_tiles = []
    for key, value in state.items():
        if key == "player" or not isinstance(value, list):
            continue
        all_tiles.extend(
            tuple(p) for p in value
            if isinstance(p, (list, tuple)) and len(p) == 2
        )

    if all_tiles:
        min_x = min(p[0] for p in all_tiles)
        max_x = max(p[0] for p in all_tiles)
        min_y = min(p[1] for p in all_tiles)
        max_y = max(p[1] for p in all_tiles)
    else:
        min_x = min_y = 0
        max_x = max_y = float("inf")

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        target = (x + dx, y + dy)

        in_bounds = (
            min_x <= target[0] <= max_x and
            min_y <= target[1] <= max_y
        )
        target_entities = entity_at(target)
        passable = (
            not target_entities or
            all(key.endswith(("grass", "sand", "path")) for key in target_entities)
        )

        if in_bounds and passable:
            new_state["player"] = [[target[0], target[1]]]
        return new_state

    dx, dy = facing
    target = (x + dx, y + dy)

    if action == "do":
        target_entities = entity_at(target)

        for key in target_entities:
            if key.endswith("tree"):
                remove_at(key, target)
                add_at("grass", target)
                new_state["inv_wood"] = new_state.get("inv_wood", 0) + 1
                new_state["ach_collect_wood"] = (
                    new_state.get("ach_collect_wood", 0) + 1
                )
                return new_state

            if key.endswith("stone") and new_state.get("inv_wood_pickaxe", 0) > 0:
                remove_at(key, target)
                add_at("path", target)
                new_state["inv_stone"] = new_state.get("inv_stone", 0) + 1
                return new_state

            if key.endswith("coal") and new_state.get("inv_wood_pickaxe", 0) > 0:
                remove_at(key, target)
                add_at("path", target)
                new_state["inv_coal"] = new_state.get("inv_coal", 0) + 1
                return new_state

            if key.endswith("iron") and new_state.get("inv_stone_pickaxe", 0) > 0:
                remove_at(key, target)
                add_at("path", target)
                new_state["inv_iron"] = new_state.get("inv_iron", 0) + 1
                return new_state

            if key.endswith("diamond") and new_state.get("inv_iron_pickaxe", 0) > 0:
                remove_at(key, target)
                add_at("path", target)
                new_state["inv_diamond"] = new_state.get("inv_diamond", 0) + 1
                return new_state

        return new_state

    if action.startswith("place_"):
        item = action[len("place_"):]
        inventory_key = "inv_" + item

        if new_state.get(inventory_key, 0) <= 0:
            return new_state

        target_entities = entity_at(target)
        terrain_only = all(
            key.endswith(("grass", "sand", "path", "water"))
            for key in target_entities
        )

        if target_entities and terrain_only:
            replace_tile(target, item)
            new_state[inventory_key] -= 1
        return new_state

    if action.startswith("make_"):
        item = action[len("make_"):]
        inventory_key = "inv_" + item

        recipes = {
            "wood_pickaxe": {"wood": 1},
            "wood_sword": {"wood": 1},
            "stone_pickaxe": {"wood": 1, "stone": 1},
            "stone_sword": {"wood": 1, "stone": 1},
            "iron_pickaxe": {"wood": 1, "coal": 1, "iron": 1},
            "iron_sword": {"wood": 1, "coal": 1, "iron": 1},
        }
        recipe = recipes.get(item)
        if recipe is None or not has_nearby("table"):
            return new_state

        if item.startswith("iron_") and not has_nearby("furnace"):
            return new_state

        if all(
            new_state.get("inv_" + material, 0) >= amount
            for material, amount in recipe.items()
        ):
            for material, amount in recipe.items():
                new_state["inv_" + material] -= amount
            new_state[inventory_key] = new_state.get(inventory_key, 0) + 1

        return new_state

    # noop, unsuccessful sleep, and unsupported actions only advance time.
    return new_state