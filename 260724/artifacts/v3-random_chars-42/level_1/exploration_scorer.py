def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    goal = max(0, min(1, after.get("ach_place_zezroc", 0) - before.get("ach_place_zezroc", 0)))
    won = int(bool(after.get("won", False))) - int(bool(before.get("won", False)))
    lost = int(bool(after.get("lost", False))) - int(bool(before.get("lost", False)))

    collect = max(0, after.get("ach_collect_tpkhxk", 0) - before.get("ach_collect_tpkhxk", 0))
    collect = collect + max(0, after.get("ach_collect_sgqeje", 0) - before.get("ach_collect_sgqeje", 0))
    collect = collect + max(0, after.get("ach_collect_bzracx", 0) - before.get("ach_collect_bzracx", 0))
    collect = collect + max(0, after.get("ach_collect_grpoqi", 0) - before.get("ach_collect_grpoqi", 0))
    collect = collect + max(0, after.get("ach_collect_mwzvua", 0) - before.get("ach_collect_mwzvua", 0))

    crafted = max(0, after.get("ach_make_tpkhxk_bcwrvm", 0) - before.get("ach_make_tpkhxk_bcwrvm", 0))
    crafted = crafted + max(0, after.get("ach_make_sgqeje_bcwrvm", 0) - before.get("ach_make_sgqeje_bcwrvm", 0))
    crafted = crafted + max(0, after.get("ach_make_bzracx_bcwrvm", 0) - before.get("ach_make_bzracx_bcwrvm", 0))
    crafted = crafted + max(0, after.get("ach_make_tpkhxk_wqiqzh", 0) - before.get("ach_make_tpkhxk_wqiqzh", 0))
    crafted = crafted + max(0, after.get("ach_make_sgqeje_wqiqzh", 0) - before.get("ach_make_sgqeje_wqiqzh", 0))
    crafted = crafted + max(0, after.get("ach_make_bzracx_wqiqzh", 0) - before.get("ach_make_bzracx_wqiqzh", 0))

    placed = max(0, after.get("ach_place_sgqeje", 0) - before.get("ach_place_sgqeje", 0))
    placed = placed + max(0, after.get("ach_place_ckqpdj", 0) - before.get("ach_place_ckqpdj", 0))

    inventory_gain = max(0, after.get("inv_tpkhxk", 0) - before.get("inv_tpkhxk", 0))
    inventory_gain = inventory_gain + max(0, after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0))
    inventory_gain = inventory_gain + max(0, after.get("inv_bzracx", 0) - before.get("inv_bzracx", 0))
    inventory_gain = inventory_gain + max(0, after.get("inv_grpoqi", 0) - before.get("inv_grpoqi", 0))
    inventory_gain = inventory_gain + max(0, after.get("inv_mwzvua", 0) - before.get("inv_mwzvua", 0))
    inventory_gain = inventory_gain + max(0, after.get("inv_wcgshh", 0) - before.get("inv_wcgshh", 0))

    health_change = max(-9, min(9, after.get("player_health", 0) - before.get("player_health", 0)))
    novelty = int(bool(search_context.get("novel_effect", False))) + int(bool(search_context.get("novel_state", False)))

    score = 12000 * goal + 15000 * won - 15000 * lost
    score = score + 250 * crafted + 120 * placed + 60 * collect
    score = score + 15 * min(20, inventory_gain)
    score = score + 20 * health_change + 2 * novelty
    return float(max(-20000, min(20000, score)))
