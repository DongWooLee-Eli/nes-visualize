def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_gain = after.get("inv_tpkhxk", 0) - before.get("inv_tpkhxk", 0)
    target_gain = max(-10, min(10, target_gain))

    target_achievement = (
        after.get("ach_collect_tpkhxk", 0)
        - before.get("ach_collect_tpkhxk", 0)
    )
    target_achievement = max(-1, min(1, target_achievement))

    precursor_gain = (
        after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)
        + after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)
        + after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)
        + after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)
    )
    precursor_gain = max(-10, min(10, precursor_gain))

    tool_gain = (
        after.get("inv_tpkhxk_bcwrvm", 0)
        - before.get("inv_tpkhxk_bcwrvm", 0)
        + after.get("inv_tpkhxk_wqiqzh", 0)
        - before.get("inv_tpkhxk_wqiqzh", 0)
    )
    tool_gain = max(-4, min(4, tool_gain))

    health_change = (
        after.get("player_health", 0)
        - before.get("player_health", 0)
    )
    health_change = max(-9, min(9, health_change))

    won_gain = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    lost_gain = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))

    novelty = (
        int(bool(search_context.get("novel_effect", False)))
        + int(bool(search_context.get("novel_state", False)))
    )

    score = (
        100.0 * target_gain
        + 150.0 * target_achievement
        + 3.0 * precursor_gain
        + 2.0 * tool_gain
        + 4.0 * health_change
        + 500.0 * won_gain
        - 500.0 * lost_gain
        + 0.5 * novelty
    )
    return float(max(-1000.0, min(1000.0, score)))
