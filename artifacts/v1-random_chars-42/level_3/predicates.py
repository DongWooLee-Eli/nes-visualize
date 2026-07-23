def completed(state, result):
    """True when the specified achievement has been completed."""
    return bool(state.get(result, 0))