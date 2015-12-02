Reviews highlight 3 main issues:
* Useful rules may be hard to create. Many rules are widely applicable, but rules embedding domain-specific knowledge (dsk) perform better. Taken to the extreme: to write fully accurate integrity checks, one must know exactly what to validate. But extraction rules, unlike integrity checks, allow users to control the accuracy/amount-of-dsk trade-off.
  One could also build collections of rules by pooling and applying many user-written rules (with small performance costs). This could lead to the elaboration of R1's "meta-rules".
* Computing expansions may be costly. Fortunately, our system allows optimizations: rules can keep state between invocations, so e.g. it is easy to add caching.
* High-dimensional datasets may be a problem. But relevant rules can be selected on a subset of the data, or on-the-fly. This happens in histogram generation—uninteresting histograms are discarded after processing a few tuples—and correlation detection.
Extended response: http://git.io/icde16
