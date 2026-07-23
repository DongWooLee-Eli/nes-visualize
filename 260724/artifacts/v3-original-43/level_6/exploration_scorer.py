def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_achievement = (
        int(bool(after.get("ach_make_stone_pickaxe", 0)))
        - int(bool(before.get("ach_make_stone_pickaxe", 0)))
    )
    stone_pickaxe_change = max(
        -4,
        min(
            4,
            after.get("inv_stone_pickaxe", 0)
            - before.get("inv_stone_pickaxe", 0),
        ),
    )
    collect_stone = (
        int(bool(after.get("ach_collect_stone", 0)))
        - int(bool(before.get("ach_collect_stone", 0)))
    )
    stone_change = max(
        -16,
        min(16, after.get("inv_stone", 0) - before.get("inv_stone", 0)),
    )
    wood_pickaxe_achievement = (
        int(bool(after.get("ach_make_wood_pickaxe", 0)))
        - int(bool(before.get("ach_make_wood_pickaxe", 0)))
    )
    wood_pickaxe_change = max(
        -4,
        min(
            4,
            after.get("inv_wood_pickaxe", 0)
            - before.get("inv_wood_pickaxe", 0),
        ),
    )
    table_achievement = (
        int(bool(after.get("ach_place_table", 0)))
        - int(bool(before.get("ach_place_table", 0)))
    )
    collect_wood = (
        int(bool(after.get("ach_collect_wood", 0)))
        - int(bool(before.get("ach_collect_wood", 0)))
    )
    wood_change = max(
        -16,
        min(16, after.get("inv_wood", 0) - before.get("inv_wood", 0)),
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
        9000.0 * target_achievement
        + 9000.0 * stone_pickaxe_change
        + 1200.0 * collect_stone
        + 120.0 * stone_change
        + 700.0 * wood_pickaxe_achievement
        + 400.0 * wood_pickaxe_change
        + 350.0 * table_achievement
        + 180.0 * collect_wood
        + 15.0 * wood_change
        + 5.0 * health_change
        + 3000.0 * won_gain
        - 7000.0 * lost_gain
        + novelty
    )
    return float(max(-10000.0, min(10000.0, score)))
