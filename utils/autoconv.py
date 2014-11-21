def autoconv(field):
    try:
        field = int(field)
    except:
        try:
            field = float(field)
        except:
            pass

    return field
