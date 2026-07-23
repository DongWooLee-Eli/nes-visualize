def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_achievement = max(
        -1,
        min(
            1,
            after.get("ach_make_sgqeje_wqiqzh", 0)
            - before.get("ach_make_sgqeje_wqiqzh", 0),
        ),
    )
    target_inventory = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje_wqiqzh", 0)
            - before.get("inv_sgqeje_wqiqzh", 0),
        ),
    )
    sgqeje_inventory = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
        ),
    )
    tpkhxk_inventory = max(
        -16,
        min(
            16,
            after.get("inv_tpkhxk", 0)
            - before.get("inv_tpkhxk", 0),
        ),
    )
    grpoqi_inventory = max(
        -16,
        min(
            16,
            after.get("inv_grpoqi", 0)
            - before.get("inv_grpoqi", 0),
        ),
    )
    mwzvua_inventory = max(
        -16,
        min(
            16,
            after.get("inv_mwzvua", 0)
            - before.get("inv_mwzvua", 0),
        ),
    )
    sgqeje_collection = max(
        -1,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
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
    useful_placement = max(
        -3,
        min(
            3,
            after.get("ach_place_sgqeje", 0)
            - before.get("ach_place_sgqeje", 0)
            + after.get("ach_place_zezroc", 0)
            - before.get("ach_place_zezroc", 0)
            + after.get("ach_place_ckqpdj", 0)
            - before.get("ach_place_ckqpdj", 0),
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
        1000 * target_achievement
        + 700 * target_inventory
        + 80 * sgqeje_collection
        + 50 * tpkhxk_collection
        + 25 * sgqeje_inventory
        + 15 * tpkhxk_inventory
        + 8 * grpoqi_inventory
        + 8 * mwzvua_inventory
        + 20 * useful_placement
        + 5 * health_change
        + 1000 * won_change
        - 1000 * lost_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
