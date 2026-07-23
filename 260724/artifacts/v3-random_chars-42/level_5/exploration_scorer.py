def score_transition(transition: dict, search_context: dict) -> float:
    before = transition.get("before", {})
    after = transition.get("after", {})

    place_gain = max(
        0,
        min(
            1,
            after.get("ach_place_sgqeje", 0)
            - before.get("ach_place_sgqeje", 0),
        ),
    )
    collect_gain = max(
        0,
        min(
            1,
            after.get("ach_collect_sgqeje", 0)
            - before.get("ach_collect_sgqeje", 0),
        ),
    )
    inventory_change = max(
        -10,
        min(
            10,
            after.get("inv_sgqeje", 0)
            - before.get("inv_sgqeje", 0),
        ),
    )
    source_decrease = max(
        0,
        min(
            10,
            len(before.get("sgqeje", []))
            - len(after.get("sgqeje", [])),
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
    won_gain = max(
        0,
        int(bool(after.get("won", False)))
        - int(bool(before.get("won", False))),
    )
    lost_gain = max(
        0,
        int(bool(after.get("lost", False)))
        - int(bool(before.get("lost", False))),
    )
    novelty = int(bool(search_context.get("novel_effect", False)))
    novelty = novelty + int(bool(search_context.get("novel_state", False)))

    score = 18000 * place_gain
    score = score + 12000 * won_gain
    score = score - 18000 * lost_gain
    score = score + 4000 * collect_gain
    score = score + 2500 * max(0, inventory_change)
    score = score + 150 * source_decrease
    score = score + 400 * min(0, inventory_change) * (1 - place_gain)
    score = score + 25 * health_change
    score = score + 2 * novelty

    return float(max(-20000, min(20000, score)))
