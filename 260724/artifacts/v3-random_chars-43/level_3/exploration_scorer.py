def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    goal_achievement = max(
        -1,
        min(
            1,
            after.get("ach_make_tpkhxk_wqiqzh", 0)
            - before.get("ach_make_tpkhxk_wqiqzh", 0),
        ),
    )
    goal_item = max(
        -9,
        min(
            9,
            after.get("inv_tpkhxk_wqiqzh", 0)
            - before.get("inv_tpkhxk_wqiqzh", 0),
        ),
    )
    tpkhxk_item = max(
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

    resource_change = (
        after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)
        + after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)
        + after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)
        + after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)
        + after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0)
    )
    resource_change = max(-20, min(20, resource_change))

    collection_change = (
        after.get("ach_collect_bzracx", 0)
        - before.get("ach_collect_bzracx", 0)
        + after.get("ach_collect_grpoqi", 0)
        - before.get("ach_collect_grpoqi", 0)
        + after.get("ach_collect_mwzvua", 0)
        - before.get("ach_collect_mwzvua", 0)
        + after.get("ach_collect_sgqeje", 0)
        - before.get("ach_collect_sgqeje", 0)
    )
    collection_change = max(-4, min(4, collection_change))

    station_change = (
        after.get("ach_place_ckqpdj", 0)
        - before.get("ach_place_ckqpdj", 0)
        + after.get("ach_place_sgqeje", 0)
        - before.get("ach_place_sgqeje", 0)
        + after.get("ach_place_zezroc", 0)
        - before.get("ach_place_zezroc", 0)
    )
    station_change = max(-3, min(3, station_change))

    supporting_craft_change = (
        after.get("ach_make_tpkhxk_bcwrvm", 0)
        - before.get("ach_make_tpkhxk_bcwrvm", 0)
        + after.get("ach_make_sgqeje_wqiqzh", 0)
        - before.get("ach_make_sgqeje_wqiqzh", 0)
        + after.get("ach_make_bzracx_wqiqzh", 0)
        - before.get("ach_make_bzracx_wqiqzh", 0)
        + after.get("ach_make_sgqeje_bcwrvm", 0)
        - before.get("ach_make_sgqeje_bcwrvm", 0)
        + after.get("ach_make_bzracx_bcwrvm", 0)
        - before.get("ach_make_bzracx_bcwrvm", 0)
    )
    supporting_craft_change = max(-5, min(5, supporting_craft_change))

    health_change = max(
        -9,
        min(
            9,
            after.get("player_health", 0)
            - before.get("player_health", 0),
        ),
    )
    won_change = (
        int(bool(after.get("won", False)))
        - int(bool(before.get("won", False)))
    )
    lost_change = (
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
        + 20 * tpkhxk_item
        + 8 * collection_change
        + 3 * resource_change
        + 6 * station_change
        + 4 * supporting_craft_change
        + 1000 * won_change
        - 1000 * lost_change
        + 5 * health_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
