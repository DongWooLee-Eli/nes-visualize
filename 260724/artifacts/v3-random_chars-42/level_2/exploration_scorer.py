def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_achievement = max(
        0,
        min(
            1,
            after.get("ach_make_tpkhxk_bcwrvm", 0)
            - before.get("ach_make_tpkhxk_bcwrvm", 0),
        ),
    )
    target_inventory = max(
        0,
        min(
            10,
            after.get("inv_tpkhxk_bcwrvm", 0)
            - before.get("inv_tpkhxk_bcwrvm", 0),
        ),
    )

    tpkhxk_gain = max(
        0,
        min(10, after.get("inv_tpkhxk", 0) - before.get("inv_tpkhxk", 0)),
    )
    tpkhxk_collect = max(
        0,
        min(
            1,
            after.get("ach_collect_tpkhxk", 0)
            - before.get("ach_collect_tpkhxk", 0),
        ),
    )

    material_gain = max(
        0,
        min(10, after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)),
    )
    material_gain = material_gain + max(
        0,
        min(10, after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)),
    )
    material_gain = material_gain + max(
        0,
        min(10, after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)),
    )
    material_gain = material_gain + max(
        0,
        min(10, after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)),
    )
    material_gain = material_gain + max(
        0,
        min(10, after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0)),
    )

    collection_progress = max(
        0,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    collection_progress = collection_progress + max(
        0,
        min(
            1,
            after.get("ach_collect_bzracx", 0)
            - before.get("ach_collect_bzracx", 0),
        ),
    )
    collection_progress = collection_progress + max(
        0,
        min(
            1,
            after.get("ach_collect_grpoqi", 0)
            - before.get("ach_collect_grpoqi", 0),
        ),
    )
    collection_progress = collection_progress + max(
        0,
        min(
            1,
            after.get("ach_collect_mwzvua", 0)
            - before.get("ach_collect_mwzvua", 0),
        ),
    )

    station_progress = max(
        0,
        min(
            1,
            after.get("ach_place_sgqeje", 0)
            - before.get("ach_place_sgqeje", 0),
        ),
    )
    station_progress = station_progress + max(
        0,
        min(
            1,
            after.get("ach_place_ckqpdj", 0)
            - before.get("ach_place_ckqpdj", 0),
        ),
    )
    station_progress = station_progress + max(
        0,
        min(
            1,
            after.get("ach_place_zezroc", 0)
            - before.get("ach_place_zezroc", 0),
        ),
    )

    health_change = max(
        -9,
        min(
            9,
            after.get("player_health", 0) - before.get("player_health", 0),
        ),
    )
    won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))
    novelty = int(bool(search_context.get("novel_effect", False)))
    novelty = novelty + int(bool(search_context.get("novel_state", False)))

    score = 12000 * target_achievement + 8000 * target_inventory
    score = score + 180 * tpkhxk_collect + 80 * tpkhxk_gain
    score = score + 20 * material_gain + 50 * collection_progress
    score = score + 100 * station_progress + 20 * health_change
    score = score + 15000 * won - 15000 * lost + 2 * novelty
    return float(max(-20000, min(20000, score)))
