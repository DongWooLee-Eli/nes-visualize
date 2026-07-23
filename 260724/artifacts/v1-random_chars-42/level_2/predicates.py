def achieved(state, flag):
    """True when the specified achievement has been completed."""
    return bool(state.get(flag, 0))


def harvestable(state, source):
    """True when the specified harvest source exists in the world."""
    return bool(state.get(source, []))