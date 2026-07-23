def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    stone_change = int(after.get("inv_stone", 0)) - int(before.get("inv_stone", 0))
    stone_gain = max(0, min(20, stone_change))
    stone_loss = max(0, min(20, -stone_change))

    achievement_change = int(after.get("ach_collect_stone", 0)) - int(before.get("ach_collect_stone", 0))
    achievement_gain = max(0, min(1, achievement_change))

    visible_stone_change = len(before.get("stone", [])) - len(after.get("stone", []))
    visible_stone_collected = max(0, min(20, visible_stone_change))

    health_change = int(after.get("player_health", 0)) - int(before.get("player_health", 0))
    health_loss = max(0, min(20, -health_change))

    newly_won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    newly_won = max(0, min(1, newly_won))

    newly_lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))
    newly_lost = max(0, min(1, newly_lost))

    confirmed_collection = min(stone_gain, visible_stone_collected)
    mission_success = max(achievement_gain, min(1, stone_gain))

    score = 500.0 * mission_success
    score = score + 100.0 * stone_gain
    score = score + 25.0 * confirmed_collection
    score = score - 20.0 * stone_loss
    score = score - 10.0 * health_loss
    score = score + 100.0 * newly_won
    score = score - 600.0 * newly_lost

    return float(max(-600.0, min(1000.0, score)))
