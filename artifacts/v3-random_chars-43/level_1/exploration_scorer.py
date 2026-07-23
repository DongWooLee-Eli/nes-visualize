def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    goal_gain = (
        after.get("ach_place_zezroc", 0)
        - before.get("ach_place_zezroc", 0)
    )
    goal_gain = max(-1, min(1, goal_gain))

    won_gain = (
        int(bool(after.get("won", False)))
        - int(bool(before.get("won", False)))
    )
    lost_gain = (
        int(bool(after.get("lost", False)))
        - int(bool(before.get("lost", False)))
    )

    collection_gain = (
        after.get("ach_collect_bzracx", 0) - before.get("ach_collect_bzracx", 0)
        + after.get("ach_collect_grpoqi", 0) - before.get("ach_collect_grpoqi", 0)
        + after.get("ach_collect_mwzvua", 0) - before.get("ach_collect_mwzvua", 0)
        + after.get("ach_collect_sgqeje", 0) - before.get("ach_collect_sgqeje", 0)
        + after.get("ach_collect_tpkhxk", 0) - before.get("ach_collect_tpkhxk", 0)
    )
    collection_gain = max(-5, min(5, collection_gain))

    crafting_gain = (
        after.get("ach_make_bzracx_bcwrvm", 0) - before.get("ach_make_bzracx_bcwrvm", 0)
        + after.get("ach_make_bzracx_wqiqzh", 0) - before.get("ach_make_bzracx_wqiqzh", 0)
        + after.get("ach_make_sgqeje_bcwrvm", 0) - before.get("ach_make_sgqeje_bcwrvm", 0)
        + after.get("ach_make_sgqeje_wqiqzh", 0) - before.get("ach_make_sgqeje_wqiqzh", 0)
        + after.get("ach_make_tpkhxk_bcwrvm", 0) - before.get("ach_make_tpkhxk_bcwrvm", 0)
        + after.get("ach_make_tpkhxk_wqiqzh", 0) - before.get("ach_make_tpkhxk_wqiqzh", 0)
    )
    crafting_gain = max(-6, min(6, crafting_gain))

    candidate_gain = (
        after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0)
        + after.get("inv_tpkhxk", 0) - before.get("inv_tpkhxk", 0)
        + after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)
        + after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)
        + after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)
        + after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)
    )
    candidate_gain = max(-12, min(12, candidate_gain))

    health_change = (
        after.get("player_health", 0)
        - before.get("player_health", 0)
    )
    health_change = max(-9, min(9, health_change))

    novelty = (
        int(bool(search_context.get("novel_effect", False)))
        + int(bool(search_context.get("novel_state", False)))
    )

    score = (
        800.0 * goal_gain
        + 900.0 * won_gain
        - 900.0 * lost_gain
        + 15.0 * collection_gain
        + 8.0 * crafting_gain
        + 2.0 * candidate_gain
        + 5.0 * health_change
        + 0.5 * novelty
    )
    return float(max(-1000.0, min(1000.0, score)))
