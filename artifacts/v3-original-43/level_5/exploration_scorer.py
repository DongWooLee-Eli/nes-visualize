def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    place_stone_gain = (
        int(bool(after.get("ach_place_stone", 0)))
        - int(bool(before.get("ach_place_stone", 0)))
    )
    collect_stone_gain = (
        int(bool(after.get("ach_collect_stone", 0)))
        - int(bool(before.get("ach_collect_stone", 0)))
    )
    make_pickaxe_gain = (
        int(bool(after.get("ach_make_wood_pickaxe", 0)))
        - int(bool(before.get("ach_make_wood_pickaxe", 0)))
    )
    collect_wood_gain = (
        int(bool(after.get("ach_collect_wood", 0)))
        - int(bool(before.get("ach_collect_wood", 0)))
    )

    stone_change = max(
        -16,
        min(16, after.get("inv_stone", 0) - before.get("inv_stone", 0)),
    )
    wood_change = max(
        -16,
        min(16, after.get("inv_wood", 0) - before.get("inv_wood", 0)),
    )
    pickaxe_change = max(
        -4,
        min(
            4,
            after.get("inv_wood_pickaxe", 0)
            - before.get("inv_wood_pickaxe", 0),
        ),
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
        9000.0 * place_stone_gain
        + 1200.0 * collect_stone_gain
        + 250.0 * make_pickaxe_gain
        + 80.0 * collect_wood_gain
        + 120.0 * stone_change
        + 40.0 * pickaxe_change
        + 5.0 * wood_change
        + 5.0 * health_change
        + 3000.0 * won_gain
        - 6000.0 * lost_gain
        + novelty
    )
    return float(max(-10000.0, min(10000.0, score)))
