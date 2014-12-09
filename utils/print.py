import sys
from . import color

[[(1, 3)], [(2,4), (4,5)], [(0,1)]] 

def expand_hints(fields_group, hints):
    expanded_group = []

    for field_id, feature_id in fields_group:
        if field_id == 0:
            expanded_group.extend(hints[feature_id])
        else:
            expanded_group.append((field_id - 1, feature_id))

    return tuple(expanded_group)

def describe_discrepancy(fields_group, rules_descriptions, hints, x):
    expanded = expand_hints(fields_group, hints)
    
    field_ids, values, features = zip(*((field_id, x[field_id],
                                         rules_descriptions[type(x[field_id])][feature_id])
                                        for field_id, feature_id in expanded))

    if len(expanded) == 1:
        FMT = "   > Value '{}' ({}) doesn't match feature '{}'"
        msg = FMT.format(values[0], field_ids[0], features[0])
    else:
        FMT = "   > Values {} {} do not match features {}"
        msg = FMT.format(values, field_ids, features)

    return msg, features

def print_rows(outliers, model, hints, rules_descriptions, verbosity = 0, max_w = 40, header = "   "):
    SPACE = 2

    if len(outliers) == 0:
        return

    # each outlier is (x, X, discrepancies)
    nb_fields = len(outliers[0][0])
    widths = (0,) * nb_fields

    # Compute the ideal column width for each column 
    for x, _, _ in outliers:
        widths = tuple(max(w, min(max_w, len(str(f))))
                       for w, f in zip(widths, x))

    for x, X, discrepancies in outliers:
        highlight = [field_id for fields_group in discrepancies
                              for field_id, _ in expand_hints(fields_group, hints)]
        
        truncated_x = tuple(str(f)[:w] for f, w in zip(x, widths))
        padding = tuple(w - len(f) for f, w in zip(truncated_x, widths))
        colorized_x = colorize(truncated_x, highlight)
        colorized_x = " ".join(f + " " * p for f, p in zip(colorized_x, padding))
        
        sys.stdout.write(header + colorized_x + "\n")

        if verbosity > 0:
            for fields_group in discrepancies:
                msg, features_desc = describe_discrepancy(fields_group,
                                                          rules_descriptions,
                                                          hints, x)
                sys.stdout.write(msg + "\n")
                
                if verbosity > 1:
                    model.more_info(fields_group, features_desc, X, "     ")

            sys.stdout.write("\n")
            
def colorize(row, indices):
    row = [str(f) for f in row]
    for index in indices:
        row[index] = color.highlight(row[index], color.term.UNDERLINE)
    return row
