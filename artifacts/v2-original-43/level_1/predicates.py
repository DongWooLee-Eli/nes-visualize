def achieved(state, *args):
    """True when the requested achievement has been recorded."""
    if len(args) < 1:
        return False
    result = args[0]
    return bool(state.get(result, False))


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


def tree(state, *args):
    """True when the target denotes a tree resource present in the state."""
    if len(args) < 1:
        return False

    target = args[0]
    if not isinstance(target, str) or not target.endswith("tree"):
        return False

    positions = state.get(target, [])
    return isinstance(positions, list) and len(positions) > 0