def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    wood_before = int(before.get("inv_wood", 0))
    wood_after = int(after.get("inv_wood", 0))
    wood_gain = wood_after - wood_before
    wood_gain = max(-16, min(16, wood_gain))

    achievement_before = int(before.get("ach_collect_wood", 0))
    achievement_after = int(after.get("ach_collect_wood", 0))
    achievement_gain = max(0, min(1, achievement_after - achievement_before))

    trees_before = len(before.get("tree", []))
    trees_after = len(after.get("tree", []))
    trees_removed = max(0, min(16, trees_before - trees_after))

    health_before = int(before.get("player_health", 0))
    health_after = int(after.get("player_health", 0))
    health_change = max(-20, min(20, health_after - health_before))

    newly_won = bool(after.get("won", False)) and not bool(before.get("won", False))
    newly_lost = bool(after.get("lost", False)) and not bool(before.get("lost", False))

    score = 12.0 * wood_gain
    score = score + 40.0 * achievement_gain
    if wood_gain > 0 and trees_removed > 0:
        score = score + 2.0 * min(wood_gain, trees_removed)
    if health_change < 0:
        score = score + 0.5 * health_change
    if newly_won:
        score = score + 50.0
    if newly_lost:
        score = score - 100.0

    return float(max(-200.0, min(200.0, score)))
