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
        return new_state.get(key, []) or []

    def contains(key, pos):
        return list(pos) in positions(key)

    def add_position(key, pos):
        new_state.setdefault(key, [])
        if list(pos) not in new_state[key]:
            new_state[key].append(list(pos))
            new_state[key].sort(key=lambda p: (p[0], p[1]))

    def remove_position(key, pos):
        if key in new_state:
            new_state[key] = [p for p in new_state[key] if p != list(pos)]

    def coordinate_keys():
        for key, value in new_state.items():
            if key == "player" or key.startswith("inv_"):
                continue
            if (
                isinstance(value, list)
                and value
                and all(
                    isinstance(p, (list, tuple))
                    and len(p) == 2
                    and all(isinstance(v, (int, float)) for v in p)
                    for p in value
                )
            ):
                yield key

    def entity_at(pos):
        return [key for key in coordinate_keys() if contains(key, pos)]

    def is_ground(key):
        return (
            key.endswith("grass")
            or key.endswith("sand")
            or key.endswith("path")
            or key.endswith("floor")
        )

    def is_inside_world(pos):
        return any(contains(key, pos) for key in coordinate_keys())

    def is_walkable(pos):
        keys = entity_at(pos)
        if not keys or not any(is_ground(key) for key in keys):
            return False

        for key in keys:
            if is_ground(key):
                continue
            if (
                key.endswith("water")
                or key.endswith("tree")
                or key.endswith("stone")
                or key.endswith("coal")
                or key.endswith("iron")
                or key.endswith("diamond")
                or key.endswith("table")
                or key.endswith("furnace")
                or key.endswith("plant")
                or key.endswith("door")
                or key.startswith("closed_")
            ):
                return False
        return True

    player = new_state.get("player", [])
    if not player:
        return new_state

    x, y = player[0]

    # Moving always changes facing, even when the destination is blocked.
    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        target = [x + dx, y + dy]

        if (
            not new_state.get("player_sleeping", False)
            and is_inside_world(target)
            and is_walkable(target)
        ):
            new_state["player"] = [target]
        return new_state

    facing = new_state.get("player_facing", [0, 1])
    if not isinstance(facing, list) or len(facing) != 2:
        facing = [0, 1]
    target = [x + facing[0], y + facing[1]]

    if action == "do":
        # Harvest the entity directly in front of the player.
        for key in list(coordinate_keys()):
            if not contains(key, target):
                continue

            if key.endswith("tree"):
                remove_position(key, target)
                add_position("grass", target)
                new_state["inv_wood"] = new_state.get("inv_wood", 0) + 1
                new_state["ach_collect_wood"] = max(
                    new_state.get("ach_collect_wood", 0), 1
                )
                break

            if key.endswith("stone") and new_state.get("inv_wood_pickaxe", 0) > 0:
                remove_position(key, target)
                add_position("grass", target)
                new_state["inv_stone"] = new_state.get("inv_stone", 0) + 1
                break

            if key.endswith("coal") and new_state.get("inv_wood_pickaxe", 0) > 0:
                remove_position(key, target)
                add_position("grass", target)
                new_state["inv_coal"] = new_state.get("inv_coal", 0) + 1
                break

            if key.endswith("iron") and new_state.get("inv_stone_pickaxe", 0) > 0:
                remove_position(key, target)
                add_position("grass", target)
                new_state["inv_iron"] = new_state.get("inv_iron", 0) + 1
                break

            if key.endswith("diamond") and new_state.get("inv_iron_pickaxe", 0) > 0:
                remove_position(key, target)
                add_position("grass", target)
                new_state["inv_diamond"] = new_state.get("inv_diamond", 0) + 1
                break

        return new_state

    if action.startswith("place_"):
        placed = action[len("place_"):]
        costs = {
            "stone": {"inv_stone": 1},
            "table": {"inv_wood": 2},
            "furnace": {"inv_stone": 4},
            "plant": {"inv_sapling": 1},
        }
        cost = costs.get(placed)

        if cost and is_walkable(target):
            affordable = all(
                new_state.get(item, 0) >= amount
                for item, amount in cost.items()
            )
            if affordable:
                for item, amount in cost.items():
                    new_state[item] -= amount
                for key in list(coordinate_keys()):
                    if is_ground(key):
                        remove_position(key, target)
                add_position(placed, target)
        return new_state

    if action.startswith("make_"):
        item = action[len("make_"):]
        recipes = {
            "wood_pickaxe": {"inv_wood": 1},
            "stone_pickaxe": {"inv_wood": 1, "inv_stone": 1},
            "iron_pickaxe": {
                "inv_wood": 1,
                "inv_coal": 1,
                "inv_iron": 1,
            },
            "wood_sword": {"inv_wood": 1},
            "stone_sword": {"inv_wood": 1, "inv_stone": 1},
            "iron_sword": {
                "inv_wood": 1,
                "inv_coal": 1,
                "inv_iron": 1,
            },
        }
        recipe = recipes.get(item)

        # Tool crafting generally requires a nearby table.
        nearby = {
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
            (x, y),
        }
        has_table = any(
            key.endswith("table")
            and any(tuple(p) in nearby for p in positions(key))
            for key in coordinate_keys()
        )

        if recipe and has_table:
            affordable = all(
                new_state.get(resource, 0) >= amount
                for resource, amount in recipe.items()
            )
            if affordable:
                for resource, amount in recipe.items():
                    new_state[resource] -= amount
                inventory_key = "inv_" + item
                new_state[inventory_key] = new_state.get(inventory_key, 0) + 1
        return new_state

    if action == "sleep":
        new_state["player_sleeping"] = True
        return new_state

    # noop and unsupported/failed actions only advance step_count.
    return new_state