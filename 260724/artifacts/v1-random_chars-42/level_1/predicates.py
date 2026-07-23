def is_achieved(state, *args):
    """True when the specified achievement has a positive completion value."""
    if not args:
        return False
    result = args[0]
    return bool(state.get(result, 0))