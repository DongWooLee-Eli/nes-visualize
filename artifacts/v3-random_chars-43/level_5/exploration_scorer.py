def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    placed = max(
        -1,
        min(
            1,
            after.get("ach_place_sgqeje", 0)
            - before.get("ach_place_sgqeje", 0),
        ),
    )
    collected = max(
        -1,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    inventory_gain = max(
        -16,
        min(
            16,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
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
        1000 * placed
        + 150 * collected
        + 40 * inventory_gain
        + 1000 * won_change
        - 1000 * lost_change
        + 5 * health_change
        + novelty
    )
    return float(max(-1000, min(1000, score)))
