def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    wood_before = before.get("inv_wood", 0)
    wood_after = after.get("inv_wood", 0)
    wood_gain = max(-16, min(16, wood_after - wood_before))

    achievement_before = bool(before.get("ach_collect_wood", 0))
    achievement_after = bool(after.get("ach_collect_wood", 0))
    achievement_gain = int(achievement_after) - int(achievement_before)

    health_before = before.get("player_health", 0)
    health_after = after.get("player_health", 0)
    health_change = max(-16, min(16, health_after - health_before))

    won_gain = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    lost_gain = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))

    novelty = (
        0.05 * float(bool(search_context.get("novel_effect", False)))
        + 0.01 * float(bool(search_context.get("novel_state", False)))
    )

    score = (
        20.0 * wood_gain
        + 100.0 * achievement_gain
        + 500.0 * won_gain
        - 500.0 * lost_gain
        + 2.0 * health_change
        + novelty
    )
    return float(max(-1000.0, min(1000.0, score)))
