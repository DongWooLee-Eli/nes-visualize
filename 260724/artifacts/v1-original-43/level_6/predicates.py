def available(state, *args):
    """True when the specified resource has at least one available map location."""
    if not args:
        return False
    resource = args[0]
    locations = state.get(resource, [])
    return isinstance(locations, list) and len(locations) > 0


def is_set(state, *args):
    """True when the specified achievement has been completed at least once."""
    if not args:
        return False
    achievement = args[0]
    return bool(state.get(achievement, 0))