def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    goal_achievement = max(
        -1,
        min(
            1,
            after.get("ach_make_tpkhxk_bcwrvm", 0)
            - before.get("ach_make_tpkhxk_bcwrvm", 0),
        ),
    )
    goal_item = max(
        -9,
        min(
            9,
            after.get("inv_tpkhxk_bcwrvm", 0)
            - before.get("inv_tpkhxk_bcwrvm", 0),
        ),
    )

    tpkhxk_progress = max(
        -9,
        min(
            9,
            after.get("inv_tpkhxk", 0)
            - before.get("inv_tpkhxk", 0),
        ),
    )
    tpkhxk_collection = max(
        -1,
        min(
            1,
            after.get("ach_collect_tpkhxk", 0)
            - before.get("ach_collect_tpkhxk", 0),
        ),
    )

    resource_progress = (
        after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)
        + after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)
        + after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)
        + after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)
        + after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0)
    )
    resource_progress = max(-20, min(20, resource_progress))

    collection_progress = (
        after.get("ach_collect_bzracx", 0) - before.get("ach_collect_bzracx", 0)
        + after.get("ach_collect_grpoqi", 0) - before.get("ach_collect_grpoqi", 0)
        + after.get("ach_collect_mwzvua", 0) - before.get("ach_collect_mwzvua", 0)
        + after.get("ach_collect_sgqeje", 0) - before.get("ach_collect_sgqeje", 0)
    )
    collection_progress = max(-4, min(4, collection_progress))

    station_progress = (
        after.get("ach_place_ckqpdj", 0) - before.get("ach_place_ckqpdj", 0)
        + after.get("ach_place_sgqeje", 0) - before.get("ach_place_sgqeje", 0)
        + after.get("ach_place_zezroc", 0) - before.get("ach_place_zezroc", 0)
    )
    station_progress = max(-3, min(3, station_progress))

    supporting_crafts = (
        after.get("ach_make_bzracx_bcwrvm", 0)
        - before.get("ach_make_bzracx_bcwrvm", 0)
        + after.get("ach_make_bzracx_wqiqzh", 0)
        - before.get("ach_make_bzracx_wqiqzh", 0)
        + after.get("ach_make_sgqeje_bcwrvm", 0)
        - before.get("ach_make_sgqeje_bcwrvm", 0)
        + after.get("ach_make_sgqeje_wqiqzh", 0)
        - before.get("ach_make_sgqeje_wqiqzh", 0)
        + after.get("ach_make_tpkhxk_wqiqzh", 0)
        - before.get("ach_make_tpkhxk_wqiqzh", 0)
    )
    supporting_crafts = max(-5, min(5, supporting_crafts))

    health_change = max(
        -9,
        min(
            9,
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
        int(bool(search_context.get("novel_effect", False)))
        + int(bool(search_context.get("novel_state", False)))
    )

    score = (
        1000 * goal_achievement
        + 700 * goal_item
        + 80 * tpkhxk_collection
        + 20 * tpkhxk_progress
        + 8 * collection_progress
        + 3 * resource_progress
        + 6 * station_progress
        + 4 * supporting_crafts
        + 1000 * won_gain
        - 1000 * lost_gain
        + 5 * health_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
