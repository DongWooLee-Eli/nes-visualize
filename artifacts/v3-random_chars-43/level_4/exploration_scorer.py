def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    goal_achievement = max(
        -1,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    goal_inventory = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
        ),
    )

    supporting_inventory = max(
        -32,
        min(
            32,
            after.get("inv_bzracx", 0)
            - before.get("inv_bzracx", 0)
            + after.get("inv_grpoqi", 0)
            - before.get("inv_grpoqi", 0)
            + after.get("inv_mwzvua", 0)
            - before.get("inv_mwzvua", 0)
            + after.get("inv_tpkhxk", 0)
            - before.get("inv_tpkhxk", 0)
            + after.get("inv_wcgshh", 0)
            - before.get("inv_wcgshh", 0),
        ),
    )

    supporting_achievements = max(
        -4,
        min(
            4,
            after.get("ach_collect_bzracx", 0)
            - before.get("ach_collect_bzracx", 0)
            + after.get("ach_collect_grpoqi", 0)
            - before.get("ach_collect_grpoqi", 0)
            + after.get("ach_collect_mwzvua", 0)
            - before.get("ach_collect_mwzvua", 0)
            + after.get("ach_collect_tpkhxk", 0)
            - before.get("ach_collect_tpkhxk", 0),
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
        900 * goal_achievement
        + 120 * goal_inventory
        + 8 * supporting_achievements
        + 2 * supporting_inventory
        + 1000 * won_change
        - 1000 * lost_change
        + 4 * health_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
