def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_achievement = max(
        0,
        min(
            1,
            after.get("ach_make_sgqeje_bcwrvm", 0)
            - before.get("ach_make_sgqeje_bcwrvm", 0),
        ),
    )
    target_inventory = max(
        -10,
        min(
            10,
            after.get("inv_sgqeje_bcwrvm", 0)
            - before.get("inv_sgqeje_bcwrvm", 0),
        ),
    )
    sgqeje_inventory = max(
        -10,
        min(
            10,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
        ),
    )
    sgqeje_collection = max(
        0,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    source_decrease = max(
        0,
        min(
            10,
            len(before.get("sgqeje", []))
            - len(after.get("sgqeje", [])),
        ),
    )
    health_change = max(
        -9,
        min(
            9,
            after.get("player_health", 0)
            - before.get("player_health", 0),
        ),
    )
    won_gain = max(
        0,
        int(bool(after.get("won", False)))
        - int(bool(before.get("won", False))),
    )
    lost_gain = max(
        0,
        int(bool(after.get("lost", False)))
        - int(bool(before.get("lost", False))),
    )
    novelty = int(bool(search_context.get("novel_effect", False)))
    novelty = novelty + int(bool(search_context.get("novel_state", False)))

    score = 18000 * target_achievement
    score = score + 12000 * max(0, target_inventory)
    score = score + 12000 * won_gain
    score = score - 20000 * lost_gain
    score = score + 2500 * sgqeje_collection
    score = score + 1200 * max(0, sgqeje_inventory)
    score = score + 100 * source_decrease
    score = score + 300 * min(0, target_inventory)
    score = score + 80 * min(0, sgqeje_inventory) * (1 - target_achievement)
    score = score + 30 * health_change
    score = score + 2 * novelty

    return float(max(-20000, min(20000, score)))
