def collected_stone(state, *args):
    """True once the player has successfully collected stone."""
    return state.get("ach_collect_stone", 0) > 0


def collected_wood(state, *args):
    """True once the player has successfully collected wood."""
    return state.get("ach_collect_wood", 0) > 0


def stone_sword_made(state, *args):
    """True once the player has successfully crafted a stone sword."""
    return state.get("ach_make_stone_sword", 0) > 0


def table_placed(state, *args):
    """True once the player has successfully placed a crafting table."""
    return state.get("ach_place_table", 0) > 0


def wood_pickaxe_made(state, *args):
    """True once the player has successfully crafted a wood pickaxe."""
    return state.get("ach_make_wood_pickaxe", 0) > 0