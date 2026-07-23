def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    table_achievement_gain = (
        int(bool(after.get("ach_place_table", 0)))
        - int(bool(before.get("ach_place_table", 0)))
    )
    table_count_gain = max(
        -16,
        min(16, len(after.get("table", [])) - len(before.get("table", [])))
    )

    wood_gain = max(
        -16,
        min(16, after.get("inv_wood", 0) - before.get("inv_wood", 0))
    )
    wood_achievement_gain = (
        int(bool(after.get("ach_collect_wood", 0)))
        - int(bool(before.get("ach_collect_wood", 0)))
    )

    health_change = max(
        -16,
        min(
            16,
            after.get("player_health", 0) - before.get("player_health", 0)
        )
    )
    won_gain = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    lost_gain = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))

    novelty = (
        0.05 * float(bool(search_context.get("novel_effect", False)))
        + 0.01 * float(bool(search_context.get("novel_state", False)))
    )

    score = (
        2000.0 * table_achievement_gain
        + 1000.0 * table_count_gain
        + 25.0 * wood_gain
        + 100.0 * wood_achievement_gain
        + 3000.0 * won_gain
        - 3000.0 * lost_gain
        + 2.0 * health_change
        + novelty
    )
    return float(max(-10000.0, min(10000.0, score)))
