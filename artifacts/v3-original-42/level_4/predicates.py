def _positive(state, key):
    """Return whether a numeric or truthy state value indicates possession."""
    value = state.get(key, 0)
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return bool(value)


def _has_map_object(state, suffix):
    """Return whether any non-empty spatial state key ends with suffix."""
    return any(
        key.endswith(suffix) and isinstance(value, list) and bool(value)
        for key, value in state.items()
    )


def ach_collect_stone(state, *args):
    """True once stone has been collected."""
    return _positive(state, "ach_collect_stone") or _positive(state, "inv_stone")


def ach_collect_wood(state, *args):
    """True once wood has been collected or used to create an artifact."""
    return (
        _positive(state, "ach_collect_wood")
        or _positive(state, "inv_wood")
        or _positive(state, "inv_wood_pickaxe")
        or _positive(state, "inv_wood_sword")
        or _has_map_object(state, "table")
    )


def ach_make_wood_pickaxe(state, *args):
    """True once a wood pickaxe has been crafted."""
    return (
        _positive(state, "ach_make_wood_pickaxe")
        or _positive(state, "inv_wood_pickaxe")
    )


def ach_make_wood_sword(state, *args):
    """True once a wood sword has been crafted."""
    return (
        _positive(state, "ach_make_wood_sword")
        or _positive(state, "inv_wood_sword")
    )


def ach_place_table(state, *args):
    """True once a crafting table has been placed."""
    return _positive(state, "ach_place_table") or _has_map_object(state, "table")