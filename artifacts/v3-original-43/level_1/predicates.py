def _positions(state, key):
    """Return normalized coordinate tuples stored under a raw-state key."""
    value = state.get(key, [])
    if not isinstance(value, (list, tuple)):
        return set()

    positions = set()
    for item in value:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            positions.add(tuple(item))
    return positions


def _entity_exists(state, entity_name):
    """True when any coordinate layer for the named entity is nonempty."""
    for key, value in state.items():
        if key == entity_name or key.endswith("_" + entity_name):
            if _positions(state, key):
                return True
    return False


def grass_at(state, *args):
    """True when grass exists at the supplied coordinate, or anywhere abstractly."""
    where = args[0] if args else None

    if isinstance(where, (list, tuple)) and len(where) == 2:
        return tuple(where) in _positions(state, "grass")

    return _entity_exists(state, "grass")


def player_at(state, *args):
    """True when the actor occupies the given coordinate or terrain layer."""
    who = args[0] if len(args) > 0 else "player"
    where = args[1] if len(args) > 1 else None

    player_key = who if isinstance(who, str) and who in state else "player"
    player_positions = _positions(state, player_key)
    if not player_positions:
        return False

    if isinstance(where, (list, tuple)) and len(where) == 2:
        return tuple(where) in player_positions

    if isinstance(where, str) and _positions(state, where):
        return bool(player_positions & _positions(state, where))

    return True


def table_at(state, *args):
    """True when a table exists at the supplied coordinate, or anywhere abstractly."""
    where = args[0] if args else None
    table_positions = _positions(state, "table")

    if isinstance(where, (list, tuple)) and len(where) == 2:
        return tuple(where) in table_positions

    return bool(table_positions) or state.get("ach_place_table", 0) > 0


def tree_at(state, *args):
    """True when a tree exists at the supplied coordinate, or anywhere abstractly."""
    where = args[0] if args else None

    if isinstance(where, (list, tuple)) and len(where) == 2:
        return tuple(where) in _positions(state, "tree")

    return _entity_exists(state, "tree")