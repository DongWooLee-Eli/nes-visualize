def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    target_achievement = max(
        -1,
        min(
            1,
            after.get("ach_make_sgqeje_bcwrvm", 0)
            - before.get("ach_make_sgqeje_bcwrvm", 0),
        ),
    )
    target_gain = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje_bcwrvm", 0)
            - before.get("inv_sgqeje_bcwrvm", 0),
        ),
    )
    sgqeje_gain = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
        ),
    )
    sgqeje_collected = max(
        -1,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    grpoqi_gain = max(
        -16,
        min(
            16,
            after.get("inv_grpoqi", 0)
            - before.get("inv_grpoqi", 0),
        ),
    )
    mwzvua_gain = max(
        -16,
        min(
            16,
            after.get("inv_mwzvua", 0)
            - before.get("inv_mwzvua", 0),
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
        + 500 * target_gain
        + 80 * sgqeje_collected
        + 30 * sgqeje_gain
        + 10 * grpoqi_gain
        + 10 * mwzvua_gain
        + 1000 * won_change
        - 1000 * lost_change
        + 5 * health_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
