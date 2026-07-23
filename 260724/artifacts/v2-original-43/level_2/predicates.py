def achieved(state, *args):
    """True when the requested achievement is recorded or observable."""
    if not args:
        return False

    result = args[0]

    # Prefer an explicitly recorded persistent achievement.
    if bool(state.get(result, False)):
        return True

    if not isinstance(result, str) or not result.startswith("ach_"):
        return False

    achievement = result[len("ach_"):]

    # Collection and crafting achievements can be observed in inventory.
    inventory_key = "inv_" + achievement.removeprefix("collect_").removeprefix("make_")
    if result.startswith(("ach_collect_", "ach_make_")):
        return state.get(inventory_key, 0) > 0

    # Placement achievements can be observed on the map.
    if result.startswith("ach_place_"):
        object_name = achievement.removeprefix("place_")
        for key, value in state.items():
            if key == object_name or key.endswith("_" + object_name):
                if isinstance(value, list) and len(value) > 0:
                    return True

    return False


def adjacent_to(state, *args):
    """True when the actor is on or immediately beside the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not isinstance(actor_positions, list) or not isinstance(target_positions, list):
        return False

    def valid_position(position):
        return (
            isinstance(position, (list, tuple))
            and len(position) == 2
            and all(isinstance(value, (int, float)) for value in position)
        )

    for actor_position in actor_positions:
        if not valid_position(actor_position):
            continue
        ax, ay = actor_position

        for target_position in target_positions:
            if not valid_position(target_position):
                continue
            tx, ty = target_position

            # The low-level world treats all eight surrounding cells as nearby.
            if max(abs(ax - tx), abs(ay - ty)) <= 1:
                return True

    return False


def tree(state, *args):
    """True when the resource argument denotes an existing tree resource."""
    if not args:
        return False

    target = args[0]
    if not isinstance(target, str):
        return False

    value = state.get(target)
    if isinstance(value, list) and len(value) > 0:
        return target == "tree" or target.endswith("_tree")

    return False