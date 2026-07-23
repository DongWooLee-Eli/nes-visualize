def achieved(state, *args):
    """True when the requested achievement is recorded or evidenced in state."""
    if not args:
        return False

    result = args[0]

    # Prefer an explicit achievement flag when the world model provides one.
    if bool(state.get(result, False)):
        return True

    # Infer achievements that the low-level transition model does not update.
    inventory_evidence = {
        "ach_collect_wood": "inv_wood",
        "ach_make_wood_pickaxe": "inv_wood_pickaxe",
        "ach_make_wood_sword": "inv_wood_sword",
    }
    inventory_key = inventory_evidence.get(result)
    if inventory_key is not None and state.get(inventory_key, 0) > 0:
        return True

    placement_evidence = {
        "ach_place_table": "table",
    }
    object_name = placement_evidence.get(result)
    if object_name is not None:
        for key, value in state.items():
            if (key == object_name or key.endswith(object_name)) and value:
                return True

    return False


def adjacent_to(state, *args):
    """True when an actor occupies a cardinally adjacent tile to a resource."""
    if len(args) < 2:
        return False

    actor, target = args[0], args[1]

    def positions_for(name):
        positions = []
        for key, value in state.items():
            if key != name and not key.endswith(name):
                continue
            if not isinstance(value, list):
                continue
            for item in value:
                if (
                    isinstance(item, (list, tuple))
                    and len(item) == 2
                    and all(isinstance(v, (int, float)) for v in item)
                ):
                    positions.append((item[0], item[1]))
        return positions

    actor_positions = positions_for(actor)
    target_positions = positions_for(target)

    return any(
        abs(ax - tx) + abs(ay - ty) == 1
        for ax, ay in actor_positions
        for tx, ty in target_positions
    )


def tree(state, *args):
    """True when the resource argument denotes at least one existing tree."""
    if not args:
        return False

    target = args[0]
    for key, value in state.items():
        if (key == target or key.endswith(target)) and key.endswith("tree"):
            if isinstance(value, list) and len(value) > 0:
                return True

    return False