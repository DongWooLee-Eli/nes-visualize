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
        return pos in positions(key)

    def remove_at(key, pos):
        if contains(key, pos):
            new_state[key].remove(pos)
            return True
        return False

    def add_at(key, pos):
        new_state.setdefault(key, [])
        if pos not in new_state[key]:
            new_state[key].append(pos)
            new_state[key].sort(key=lambda p: (p[0], p[1]))

    def tile_key_at(pos):
        ignored = {"player", "player_facing"}
        for key, value in new_state.items():
            if key in ignored or key.startswith("inv_"):
                continue
            if isinstance(value, list) and pos in value:
                return key
        return None

    def map_bounds():
        coords = []
        for key, value in new_state.items():
            if key == "player" or key.startswith("inv_"):
                continue
            if isinstance(value, list):
                coords.extend(
                    p for p in value
                    if isinstance(p, list) and len(p) == 2
                )
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

    def nearby(key, pos):
        return any(
            abs(other[0] - pos[0]) <= 1
            and abs(other[1] - pos[1]) <= 1
            for other in positions(key)
        )

    player = positions("player")
    if not player:
        return new_state

    x, y = player[0]

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        destination = [x + dx, y + dy]

        destination_tile = tile_key_at(destination)
        traversable = destination_tile in {"pmzjpl", "wztejd"}

        if in_bounds(destination) and traversable:
            new_state["player"] = [destination]
        return new_state

    facing = new_state.get("player_facing", [0, 1])
    target = [x + facing[0], y + facing[1]]

    if action == "do":
        tile = tile_key_at(target)
        if tile is None:
            return new_state

        collected = None
        required_tool = None
        replacement_tile = "pmzjpl"

        if tile == "xcvkpr":
            collected = "tpkhxk"
        elif tile == "sgqeje":
            collected = "sgqeje"
            required_tool = "tpkhxk_bcwrvm"
            replacement_tile = "ydtzir"
        elif tile == "grpoqi":
            collected = "grpoqi"
            required_tool = "tpkhxk_bcwrvm"
        elif tile == "bzracx":
            collected = "bzracx"
            required_tool = "sgqeje_bcwrvm"
        elif tile == "mwzvua":
            collected = "mwzvua"
            required_tool = "bzracx_bcwrvm"

        if collected is not None:
            can_collect = (
                required_tool is None
                or new_state.get("inv_" + required_tool, 0) > 0
            )
            if can_collect and remove_at(tile, target):
                add_at(replacement_tile, target)
                inv_key = "inv_" + collected
                new_state[inv_key] = new_state.get(inv_key, 0) + 1
                achievement_key = "ach_collect_" + collected
                new_state[achievement_key] = (
                    new_state.get(achievement_key, 0) + 1
                )

        return new_state

    if action.startswith("place_"):
        entity = action[len("place_"):]
        costs = {
            "sgqeje": {"sgqeje": 1},
            "zezroc": {"tpkhxk": 2},
            "ckqpdj": {"sgqeje": 4},
            "rjwdrk": {"wcgshh": 1},
        }
        cost = costs.get(entity, {entity: 1})

        target_tile = tile_key_at(target)
        can_place = (
            in_bounds(target)
            and target_tile in {"pmzjpl", "wztejd"}
            and all(
                new_state.get("inv_" + item, 0) >= amount
                for item, amount in cost.items()
            )
        )

        if can_place:
            remove_at(target_tile, target)
            add_at(entity, target)
            for item, amount in cost.items():
                key = "inv_" + item
                new_state[key] = new_state.get(key, 0) - amount
            achievement_key = "ach_place_" + entity
            new_state[achievement_key] = (
                new_state.get(achievement_key, 0) + 1
            )

        return new_state

    if action.startswith("make_"):
        output = action[len("make_"):]
        material = output.split("_", 1)[0]

        recipes = {
            "tpkhxk": {"tpkhxk": 1},
            "sgqeje": {"tpkhxk": 1, "sgqeje": 1},
            "bzracx": {"tpkhxk": 1, "grpoqi": 1, "bzracx": 1},
        }
        cost = recipes.get(material)

        can_craft = (
            cost is not None
            and nearby("zezroc", [x, y])
            and all(
                new_state.get("inv_" + item, 0) >= amount
                for item, amount in cost.items()
            )
        )

        if can_craft:
            for item, amount in cost.items():
                key = "inv_" + item
                new_state[key] = new_state.get(key, 0) - amount

            output_key = "inv_" + output
            new_state[output_key] = new_state.get(output_key, 0) + 1

            achievement_key = "ach_make_" + output
            new_state[achievement_key] = (
                new_state.get(achievement_key, 0) + 1
            )

        return new_state

    return new_state