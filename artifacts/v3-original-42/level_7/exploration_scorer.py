def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    wood_gain = max(0, min(20, int(after.get("inv_wood", 0)) - int(before.get("inv_wood", 0))))
    stone_gain = max(0, min(20, int(after.get("inv_stone", 0)) - int(before.get("inv_stone", 0))))

    wood_collected = max(0, min(1, int(after.get("ach_collect_wood", 0)) - int(before.get("ach_collect_wood", 0))))
    table_placed = max(0, min(1, int(after.get("ach_place_table", 0)) - int(before.get("ach_place_table", 0))))
    wood_pickaxe_made = max(0, min(1, int(after.get("ach_make_wood_pickaxe", 0)) - int(before.get("ach_make_wood_pickaxe", 0))))
    stone_collected = max(0, min(1, int(after.get("ach_collect_stone", 0)) - int(before.get("ach_collect_stone", 0))))
    stone_pickaxe_made = max(0, min(1, int(after.get("ach_make_stone_pickaxe", 0)) - int(before.get("ach_make_stone_pickaxe", 0))))
    stone_sword_made = max(0, min(1, int(after.get("ach_make_stone_sword", 0)) - int(before.get("ach_make_stone_sword", 0))))

    wood_pickaxe_gain = max(0, min(1, int(after.get("inv_wood_pickaxe", 0)) - int(before.get("inv_wood_pickaxe", 0))))
    stone_pickaxe_gain = max(0, min(1, int(after.get("inv_stone_pickaxe", 0)) - int(before.get("inv_stone_pickaxe", 0))))
    stone_sword_gain = max(0, min(1, int(after.get("inv_stone_sword", 0)) - int(before.get("inv_stone_sword", 0))))

    health_loss = max(0, min(20, int(before.get("player_health", 0)) - int(after.get("player_health", 0))))
    newly_lost = max(0, min(1, int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))))
    newly_won = max(0, min(1, int(bool(after.get("won", False))) - int(bool(before.get("won", False)))))

    score = 2.0 * wood_gain + 5.0 * stone_gain
    score = score + 30.0 * wood_collected
    score = score + 100.0 * table_placed
    score = score + 180.0 * wood_pickaxe_made
    score = score + 300.0 * stone_collected
    score = score + 1400.0 * stone_pickaxe_made
    score = score + 180.0 * wood_pickaxe_gain
    score = score + 1400.0 * stone_pickaxe_gain
    score = score + 10000.0 * stone_sword_made
    score = score + 10000.0 * stone_sword_gain
    score = score + 2000.0 * newly_won
    score = score - 20.0 * health_loss
    score = score - 1000.0 * newly_lost

    return float(max(-1000.0, min(22000.0, score)))
