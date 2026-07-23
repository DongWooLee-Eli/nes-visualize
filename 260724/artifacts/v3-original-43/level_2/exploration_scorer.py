def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    pickaxe_gain = max(
        -4,
        min(
            4,
            after.get("inv_wood_pickaxe", 0)
            - before.get("inv_wood_pickaxe", 0),
        ),
    )
    pickaxe_achievement_gain = (
        int(bool(after.get("ach_make_wood_pickaxe", 0)))
        - int(bool(before.get("ach_make_wood_pickaxe", 0)))
    )

    table_gain = max(
        -4,
        min(4, len(after.get("table", [])) - len(before.get("table", []))),
    )
    table_achievement_gain = (
        int(bool(after.get("ach_place_table", 0)))
        - int(bool(before.get("ach_place_table", 0)))
    )

    wood_gain = max(
        -16,
        min(16, after.get("inv_wood", 0) - before.get("inv_wood", 0)),
    )
    wood_achievement_gain = (
        int(bool(after.get("ach_collect_wood", 0)))
        - int(bool(before.get("ach_collect_wood", 0)))
    )

    health_change = max(
        -16,
        min(
            16,
            after.get("player_health", 0)
            - before.get("player_health", 0),
        ),
    )
    won_gain = (
        int(bool(after.get("won", False)))
        - int(bool(before.get("won", False)))
    )
    lost_gain = (
        int(bool(after.get("lost", False)))
        - int(bool(before.get("lost", False)))
    )

    novelty = (
        0.05 * float(bool(search_context.get("novel_effect", False)))
        + 0.01 * float(bool(search_context.get("novel_state", False)))
    )

    score = (
        6000.0 * pickaxe_achievement_gain
        + 4000.0 * pickaxe_gain
        + 1000.0 * table_achievement_gain
        + 750.0 * table_gain
        + 200.0 * wood_achievement_gain
        + 40.0 * wood_gain
        + 3000.0 * won_gain
        - 5000.0 * lost_gain
        + 3.0 * health_change
        + novelty
    )
    return float(max(-10000.0, min(10000.0, score)))
