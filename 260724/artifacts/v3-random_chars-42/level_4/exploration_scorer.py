def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    sgqeje_gain = max(
        -10,
        min(
            10,
            after.get("inv_sgqeje", 0) - before.get("inv_sgqeje", 0),
        ),
    )
    collection_gain = max(
        0,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    source_decrease = max(
        0,
        min(
            10,
            len(before.get("sgqeje", [])) - len(after.get("sgqeje", [])),
        ),
    )

    health_change = max(
        -9,
        min(
            9,
            after.get("player_health", 0) - before.get("player_health", 0),
        ),
    )
    won_change = int(bool(after.get("won", False))) - int(
        bool(before.get("won", False))
    )
    lost_change = int(bool(after.get("lost", False))) - int(
        bool(before.get("lost", False))
    )

    novelty = int(bool(search_context.get("novel_effect", False)))
    novelty = novelty + int(bool(search_context.get("novel_state", False)))

    score = 12000 * collection_gain
    score = score + 8000 * max(0, sgqeje_gain)
    score = score + 200 * source_decrease
    score = score + 500 * min(0, sgqeje_gain)
    score = score + 20 * health_change
    score = score + 15000 * won_change - 15000 * lost_change
    score = score + 2 * novelty

    return float(max(-20000, min(20000, score)))
