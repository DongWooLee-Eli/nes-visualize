def ach_collect_stone(state, *args):
    """True once the collect-stone achievement has been earned."""
    return bool(state.get("ach_collect_stone", 0))


def ach_collect_wood(state, *args):
    """True once the collect-wood achievement has been earned."""
    return bool(state.get("ach_collect_wood", 0))


def ach_make_stone_pickaxe(state, *args):
    """True once the make-stone-pickaxe achievement has been earned."""
    return bool(state.get("ach_make_stone_pickaxe", 0))


def ach_make_wood_pickaxe(state, *args):
    """True once the make-wood-pickaxe achievement has been earned."""
    return bool(state.get("ach_make_wood_pickaxe", 0))


def ach_make_wood_sword(state, *args):
    """True once the make-wood-sword achievement has been earned."""
    return bool(state.get("ach_make_wood_sword", 0))


def ach_place_stone(state, *args):
    """True once the place-stone achievement has been earned."""
    return bool(state.get("ach_place_stone", 0))


def ach_place_table(state, *args):
    """True once the place-table achievement has been earned."""
    return bool(state.get("ach_place_table", 0))