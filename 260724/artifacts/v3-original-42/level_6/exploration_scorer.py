def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    wood_achievement = max(
        0,
        min(
            1,
            int(after.get("ach_collect_wood", 0))
            - int(before.get("ach_collect_wood", 0)),
        ),
    )
    table_achievement = max(
        0,
        min(
            1,
            int(after.get("ach_place_table", 0))
            - int(before.get("ach_place_table", 0)),
        ),
    )
    wood_pickaxe_achievement = max(
        0,
        min(
            1,
            int(after.get("ach_make_wood_pickaxe", 0))
            - int(before.get("ach_make_wood_pickaxe", 0)),
        ),
    )
    stone_achievement = max(
        0,
        min(
            1,
            int(after.get("ach_collect_stone", 0))
            - int(before.get("ach_collect_stone", 0)),
        ),
    )
    stone_pickaxe_achievement = max(
        0,
        min(
            1,
            int(after.get("ach_make_stone_pickaxe", 0))
            - int(before.get("ach_make_stone_pickaxe", 0)),
        ),
    )

    wood_gain = max(
        0,
        min(
            20,
            int(after.get("inv_wood", 0)) - int(before.get("inv_wood", 0)),
        ),
    )
    stone_gain = max(
        0,
        min(
            20,
            int(after.get("inv_stone", 0)) - int(before.get("inv_stone", 0)),
        ),
    )
    wood_pickaxe_gain = max(
        0,
        min(
            1,
            int(after.get("inv_wood_pickaxe", 0))
            - int(before.get("inv_wood_pickaxe", 0)),
        ),
    )
    stone_pickaxe_gain = max(
        0,
        min(
            1,
            int(after.get("inv_stone_pickaxe", 0))
            - int(before.get("inv_stone_pickaxe", 0)),
        ),
    )

    health_loss = max(
        0,
        min(
            20,
            int(before.get("player_health", 0))
            - int(after.get("player_health", 0)),
        ),
    )
    newly_lost = max(
        0,
        min(
            1,
            int(bool(after.get("lost", False)))
            - int(bool(before.get("lost", False))),
        ),
    )

    score = 30.0 * wood_achievement
    score = score + 80.0 * table_achievement
    score = score + 120.0 * wood_pickaxe_achievement
    score = score + 160.0 * stone_achievement
    score = score + 1000.0 * stone_pickaxe_achievement
    score = score + 2.0 * wood_gain
    score = score + 4.0 * stone_gain
    score = score + 40.0 * wood_pickaxe_gain
    score = score + 1000.0 * stone_pickaxe_gain
    score = score - 15.0 * health_loss
    score = score - 600.0 * newly_lost

    return float(max(-600.0, min(1500.0, score)))
