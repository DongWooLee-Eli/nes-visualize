def _positions(state, key):
    """Return valid coordinate pairs stored under a raw-state key."""
    value = state.get(key, [])
    if not isinstance(value, (list, tuple)):
        return set()

    return {
        tuple(position)
        for position in value
        if isinstance(position, (list, tuple)) and len(position) == 2
    }


def adjacent_to(state, *args):
    """True when the actor is orthogonally adjacent to the resource."""
    if len(args) < 2:
        return False

    who, what = args[0], args[1]
    actor_positions = _positions(state, who)
    resource_positions = _positions(state, what)

    return any(
        abs(actor_x - resource_x) + abs(actor_y - resource_y) == 1
        for actor_x, actor_y in actor_positions
        for resource_x, resource_y in resource_positions
    )


def available(state, *args):
    """True when at least one instance of the resource remains in the world."""
    if not args:
        return False

    what = args[0]
    return bool(_positions(state, what))


def is_tpkhxk(state, *args):
    """True when the world resource yields the tpkhxk inventory item."""
    if not args:
        return False

    what = args[0]
    # The low-level world's harvest mapping defines xcvkpr as yielding tpkhxk.
    return what == "xcvkpr"