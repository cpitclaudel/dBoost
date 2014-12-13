def autoconv(field, floats_only = False):
    def autoconv_step(value, converters, offset):
        if offset > len(converters):
            return value

        try:
            field = converters[offset](field)
        except:
            field = autoconv_step(value, converters, offset + 1)

        return field

    converters = [float] if floats_only else [int, float]
    return autoconv_step(field, converters, 0)
