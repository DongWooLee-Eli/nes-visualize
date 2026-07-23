def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    stone_gain = max(
        -16,
        min(
            16,
            after.get("inv_stone", 0) - before.get("inv_stone", 0),
        ),
    )
    stone_achievement_gain = (
        int(bool(after.get("ach_collect_stone", 0)))
        - int(bool(before.get("ach_collect_stone", 0)))
    )

    wood_gain = max(
        -16,
        min(
            16,
            after.get("inv_wood", 0) - before.get("inv_wood", 0),
        ),
    )
    wood_pickaxe_gain = max(
        -4,
        min(
            4,
            after.get("inv_wood_pickaxe", 0)
            - before.get("inv_wood_pickaxe", 0),
        ),
    )
    wood_pickaxe_achievement_gain = (
        int(bool(after.get("ach_make_wood_pickaxe", 0)))
        - int(bool(before.get("ach_make_wood_pickaxe", 0)))
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
        9000.0 * stone_achievement_gain
        + 1800.0 * stone_gain
        + 300.0 * wood_pickaxe_achievement_gain
        + 200.0 * wood_pickaxe_gain
        + 10.0 * wood_gain
        + 3000.0 * won_gain
        - 6000.0 * lost_gain
        + 5.0 * health_change
        + novelty
    )
    return float(max(-10000.0, min(10000.0, score)))
