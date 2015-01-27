def load_country_data():
    """Loads a list of [Country, Capital, Currency name, Currency symbol]"""
    lines = []
    with open("country_data") as country_data:
        for line in country_data:
            line = line.strip().split("\t")
            lines.append(tuple(line))
    return lines

COUNTRY_DATA = load_country_data()
