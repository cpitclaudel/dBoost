def autoconv_step(field, converters, offset):
    if offset >= len(converters):
        return value

    try:
        field = converters[offset](field)
    except Exception as e:
        field = autoconv_step(field, converters, offset + 1)

    return field

def autoconv(field, floats_only = False):
    converters = [float] if floats_only else [int, float]
    return autoconv_step(field, converters, 0)
