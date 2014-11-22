import sys
from . import color

def print_rows(outliers, model, rules_descriptions, verbosity = 0, max_w = 40, header = "   "):
    SPACE = 2

    if len(outliers) == 0:
        return

    # each outlier is (x, X, failed_tests)
    nb_fields = len(outliers[0][0])
    widths = (0,) * nb_fields

    # Compute the ideal column width for each column 
    for x, _, _ in outliers:
        widths = tuple(max(w, min(max_w, len(str(f))))
                       for w, f in zip(widths, x))

    for x, X, failed_tests in outliers:
        highlight = tuple(field_id for field_id, _ in failed_tests)
        
        truncated_x = tuple(str(f)[:w] for f, w in zip(x, widths))
        padding = tuple(w - len(f) for f, w in zip(truncated_x, widths))
        colorized_x = colorize(truncated_x, highlight)
        colorized_x = " ".join(f + " " * p for f, p in zip(colorized_x, padding))
        
        sys.stdout.write(header + colorized_x + "\n")

        if verbosity > 0:
            for field_id, failed_features in failed_tests:
                feature_descs = rules_descriptions[type(x[field_id])]
                failed_features_descs = ", ".join("'{}'".format(feature_descs[feature_id])
                                                  for feature_id in failed_features)
                sys.stdout.write("   > '{}' ({}) doesn't match feature(s) {}\n"
                                 .format(x[field_id], field_id, failed_features_descs))
                if verbosity > 1:
                    for failed_feature in failed_features:
                        model.more_info(field_id, failed_feature, feature_descs[failed_feature], X, "     ")

            sys.stdout.write("\n")
            
def colorize(row, indices):
    row = [str(f) for f in row]
    for index in indices:
        row[index] = color.highlight(row[index], color.term.UNDERLINE)
    return row
