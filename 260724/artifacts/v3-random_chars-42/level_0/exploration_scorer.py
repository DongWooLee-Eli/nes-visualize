def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_gain = max(-10, min(10, after.get("inv_tpkhxk", 0) - before.get("inv_tpkhxk", 0)))
    target_achievement = max(0, min(1, after.get("ach_collect_tpkhxk", 0) - before.get("ach_collect_tpkhxk", 0)))

    sgqeje_gain = max(-10, min(10, after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0)))
    bzracx_gain = max(-10, min(10, after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0)))
    grpoqi_gain = max(-10, min(10, after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0)))
    mwzvua_gain = max(-10, min(10, after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0)))
    wcgshh_gain = max(-10, min(10, after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0)))

    health_change = max(-9, min(9, after.get("player_health", 0) - before.get("player_health", 0)))
    newly_won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    newly_lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))

    novelty = int(bool(search_context.get("novel_effect", False))) + int(bool(search_context.get("novel_state", False)))

    score = 1000 * target_gain
    score = score + 5000 * target_achievement
    score = score + 20 * max(0, sgqeje_gain)
    score = score + 20 * max(0, bzracx_gain)
    score = score + 15 * max(0, grpoqi_gain)
    score = score + 15 * max(0, mwzvua_gain)
    score = score + 10 * max(0, wcgshh_gain)
    score = score + 25 * health_change
    score = score + 10000 * newly_won
    score = score - 10000 * newly_lost
    score = score + 2 * novelty
    return float(max(-20000, min(20000, score)))
