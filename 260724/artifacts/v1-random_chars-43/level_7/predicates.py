def available(state, *args):
    """True when the specified resource is present and can be collected."""
    if not args:
        return False
    material = str(args[0])
    return bool(state.get(material, []))


def is_set(state, *args):
    """True when the specified status or achievement has been set."""
    if not args:
        return False
    flag = str(args[0])
    return bool(state.get(flag, 0))