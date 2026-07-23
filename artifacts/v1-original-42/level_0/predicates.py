def achieved(state, *args):
    """True when the requested achievement flag is set or its outcome exists."""
    if not args:
        return False

    flag = args[0]
    if bool(state.get(flag, False)):
        return True

    if not isinstance(flag, str):
        return False

    if flag.startswith("ach_collect_"):
        resource = flag[len("ach_collect_"):]
        return state.get(f"inv_{resource}", 0) > 0

    if flag.startswith("ach_make_"):
        item = flag[len("ach_make_"):]
        return state.get(f"inv_{item}", 0) > 0

    if flag.startswith("ach_place_"):
        item = flag[len("ach_place_"):]
        positions = state.get(item, [])
        return isinstance(positions, list) and len(positions) > 0

    return False


def adjacent_to(state, *args):
    """True when the actor is cardinally adjacent to the target resource."""
    if len(args) < 2:
        return False

    who, target = args[0], args[1]
    actor_positions = state.get(who, [])
    target_positions = state.get(target, [])

    if not isinstance(actor_positions, list) or not isinstance(target_positions, list):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) != 2:
            continue

        ax, ay = actor_pos
        for target_pos in target_positions:
            if not isinstance(target_pos, (list, tuple)) or len(target_pos) != 2:
                continue

            tx, ty = target_pos
            if abs(ax - tx) + abs(ay - ty) == 1:
                return True

    return False