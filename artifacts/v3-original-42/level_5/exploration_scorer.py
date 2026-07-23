def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})
    action = transition.get("action", "")

    achievement_change = int(after.get("ach_place_stone", 0)) - int(before.get("ach_place_stone", 0))
    achievement_gain = max(0, min(1, achievement_change))

    inventory_change = int(after.get("inv_stone", 0)) - int(before.get("inv_stone", 0))
    stone_spent = max(0, min(20, -inventory_change))

    visible_change = len(after.get("stone", [])) - len(before.get("stone", []))
    visible_stone_added = max(0, min(20, visible_change))

    placement_action = int(bool(action == "place_stone"))
    confirmed_placement = min(1, placement_action, stone_spent, visible_stone_added)
    mission_success = max(achievement_gain, confirmed_placement)

    health_change = int(after.get("player_health", 0)) - int(before.get("player_health", 0))
    health_loss = max(0, min(20, -health_change))

    newly_won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    newly_won = max(0, min(1, newly_won))

    newly_lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))
    newly_lost = max(0, min(1, newly_lost))

    score = 800.0 * mission_success
    score = score + 100.0 * achievement_gain
    score = score + 50.0 * confirmed_placement
    score = score - 10.0 * health_loss
    score = score + 100.0 * newly_won
    score = score - 600.0 * newly_lost

    return float(max(-600.0, min(1000.0, score)))
