def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    sword_gain = int(after.get("inv_wood_sword", 0)) - int(before.get("inv_wood_sword", 0))
    sword_gain = max(0, min(1, sword_gain))

    sword_achievement = int(after.get("ach_make_wood_sword", 0)) - int(before.get("ach_make_wood_sword", 0))
    sword_achievement = max(0, min(1, sword_achievement))

    wood_gain = int(after.get("inv_wood", 0)) - int(before.get("inv_wood", 0))
    wood_gain = max(0, min(4, wood_gain))

    wood_achievement = int(after.get("ach_collect_wood", 0)) - int(before.get("ach_collect_wood", 0))
    wood_achievement = max(0, min(1, wood_achievement))

    table_gain = len(after.get("table", [])) - len(before.get("table", []))
    table_gain = max(0, min(1, table_gain))

    table_achievement = int(after.get("ach_place_table", 0)) - int(before.get("ach_place_table", 0))
    table_achievement = max(0, min(1, table_achievement))

    health_change = int(after.get("player_health", 0)) - int(before.get("player_health", 0))
    health_loss = max(0, min(20, -health_change))

    newly_won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    newly_won = max(0, min(1, newly_won))

    newly_lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))
    newly_lost = max(0, min(1, newly_lost))

    mission_success = max(sword_gain, sword_achievement)
    table_progress = max(table_gain, table_achievement)

    score = 600.0 * mission_success
    score = score + 80.0 * table_progress
    score = score + 15.0 * wood_gain
    score = score + 25.0 * wood_achievement
    score = score + 100.0 * newly_won
    score = score - 5.0 * health_loss
    score = score - 600.0 * newly_lost

    return float(max(-600.0, min(800.0, score)))
