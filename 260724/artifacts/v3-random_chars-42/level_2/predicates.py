def resource_available(state, *args):
    """True when the specified resource exists and has an available instance."""
    if not args:
        return False

    source = str(args[0])
    value = state.get(source)

    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict, str)):
        return len(value) > 0
    if isinstance(value, (int, float)):
        return value > 0

    return bool(value)