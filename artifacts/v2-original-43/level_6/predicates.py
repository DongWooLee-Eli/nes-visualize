def achieved(state, *args):
    """True when the specified achievement has been earned."""
    if not args:
        return False
    achievement = args[0]
    return bool(state.get(achievement, 0))


def adjacent_to(state, *args):
    """True when the actor is orthogonally adjacent to the target resource."""
    if len(args) < 2:
        return False

    actor, target = args[0], args[1]
    actor_positions = state.get(actor, [])
    target_positions = state.get(target, [])

    if not isinstance(actor_positions, list) or not isinstance(target_positions, list):
        return False

    for actor_pos in actor_positions:
        if not isinstance(actor_pos, (list, tuple)) or len(actor_pos) != 2:
            continue

        for target_pos in target_positions:
            if not isinstance(target_pos, (list, tuple)) or len(target_pos) != 2:
                continue

            if (
                abs(actor_pos[0] - target_pos[0])
                + abs(actor_pos[1] - target_pos[1])
                == 1
            ):
                return True

    return False


def stone(state, *args):
    """True when the target denotes a stone resource present in the world."""
    if not args:
        return False
    target = args[0]
    positions = state.get(target, [])
    return target == "stone" and isinstance(positions, list) and bool(positions)


def tree(state, *args):
    """True when the target denotes a tree resource present in the world."""
    if not args:
        return False
    target = args[0]
    positions = state.get(target, [])
    return target == "tree" and isinstance(positions, list) and bool(positions)