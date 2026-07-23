def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    achievement_gain = int(after.get("ach_place_table", 0)) - int(before.get("ach_place_table", 0))
    achievement_gain = max(0, min(1, achievement_gain))

    tables_added = len(after.get("table", [])) - len(before.get("table", []))
    tables_added = max(0, min(1, tables_added))

    wood_gain = int(after.get("inv_wood", 0)) - int(before.get("inv_wood", 0))
    wood_gain = max(0, min(16, wood_gain))

    wood_achievement_gain = int(after.get("ach_collect_wood", 0)) - int(before.get("ach_collect_wood", 0))
    wood_achievement_gain = max(0, min(1, wood_achievement_gain))

    health_change = int(after.get("player_health", 0)) - int(before.get("player_health", 0))
    health_loss = max(0, min(20, -health_change))

    newly_won = bool(after.get("won", False)) and not bool(before.get("won", False))
    newly_lost = bool(after.get("lost", False)) and not bool(before.get("lost", False))

    success = max(achievement_gain, tables_added)
    score = 120.0 * success
    score = score + 8.0 * wood_gain
    score = score + 12.0 * wood_achievement_gain
    score = score - 2.0 * health_loss

    if newly_won:
        score = score + 50.0
    if newly_lost:
        score = score - 150.0

    return float(max(-200.0, min(200.0, score)))
