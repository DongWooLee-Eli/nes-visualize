def is_set(state, *args):
    """True when the specified status flag is set to a truthy value."""
    if not args:
        return False
    flag = args[0]
    return bool(state.get(flag, False))


def resource_present(state, *args):
    """True when the specified resource has at least one instance present."""
    if not args:
        return False
    resource = args[0]
    value = state.get(resource)
    return bool(value)