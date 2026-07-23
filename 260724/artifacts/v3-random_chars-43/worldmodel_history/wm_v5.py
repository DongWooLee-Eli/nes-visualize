from copy import deepcopy

def transition_model(state, action):
    new_state = deepcopy(state)
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

    def positions(key):
        value = new_state.get(key, [])
        if not isinstance(value, list):
            return set()
        return {
            tuple(p) for p in value
            if isinstance(p, (list, tuple)) and len(p) == 2
        }

    current = (x, y)
    ground_key = None
    ground_size = -1
    for key, value in state.items():
        if key == "player" or key.startswith("inv_"):
            continue
        ps = positions(key)
        if current in ps and len(ps) > ground_size:
            ground_key = key
            ground_size = len(ps)

    if action in directions:
        dx, dy = directions[action]
        new_state["player_facing"] = [dx, dy]
        destination = (x + dx, y + dy)

        if ground_key is not None:
            can_move = destination in positions(ground_key)
        else:
            all_cells = set()
            for key in state:
                if key != "player" and not key.startswith("inv_"):
                    all_cells.update(positions(key))
            can_move = destination in all_cells

        if can_move:
            new_state["player"] = [[destination[0], destination[1]]]

        new_state["player_sleeping"] = False
        return new_state

    if action == "do":
        facing = state.get("player_facing", [0, 1])
        if not isinstance(facing, (list, tuple)) or len(facing) != 2:
            facing = [0, 1]
        target = (x + facing[0], y + facing[1])

        # Some world entities yield a differently named inventory resource.
        harvest_yields = {
            "xcvkpr": "tpkhxk",
        }

        harvested_layer = None
        harvested_item = None

        for layer, item in harvest_yields.items():
            if target in positions(layer):
                harvested_layer = layer
                harvested_item = item
                break

        if harvested_layer is None:
            # sgqeje is terrain rather than a directly collectible entity.
            noncollectible_layers = {"sgqeje"}

            collectible_keys = []
            for key in state:
                if (
                    key != "player"
                    and not key.startswith("inv_")
                    and key not in noncollectible_layers
                    and "inv_" + key in state
                    and target in positions(key)
                ):
                    collectible_keys.append(key)

            collectible_keys.sort(key=lambda k: len(positions(k)))
            if collectible_keys:
                harvested_layer = collectible_keys[0]
                harvested_item = harvested_layer

        if harvested_layer is not None and harvested_item is not None:
            new_state[harvested_layer] = [
                p for p in new_state.get(harvested_layer, [])
                if tuple(p) != target
            ]

            inv_key = "inv_" + harvested_item
            new_state[inv_key] = state.get(inv_key, 0) + 1

            achievement_key = "ach_collect_" + harvested_item
            new_state[achievement_key] = state.get(achievement_key, 0) + 1

            if ground_key is not None and target not in positions(ground_key):
                new_state.setdefault(ground_key, []).append(list(target))
                new_state[ground_key].sort(key=lambda p: (p[0], p[1]))

        new_state["player_sleeping"] = False
        return new_state

    if action.startswith("place_"):
        entity = action[len("place_"):]
        inv_key = "inv_" + entity
        count = state.get(inv_key, 0)

        if count > 0:
            facing = state.get("player_facing", [0, 1])
            if not isinstance(facing, (list, tuple)) or len(facing) != 2:
                facing = [0, 1]
            target = (x + facing[0], y + facing[1])

            occupied = target == current
            for key in state:
                if key != "player" and not key.startswith("inv_"):
                    if target in positions(key) and key != ground_key:
                        occupied = True
                        break

            if not occupied:
                new_state[inv_key] = count - 1
                new_state.setdefault(entity, []).append(list(target))

        new_state["player_sleeping"] = False
        return new_state

    if action == "sleep":
        new_state["player_sleeping"] = True
        return new_state

    if action != "sleep":
        new_state["player_sleeping"] = False

    return new_state