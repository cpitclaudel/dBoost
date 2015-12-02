We thank their reviewers for their detailed suggestions and for their excellent feedback. The reviews collectively point out two main perceived weaknesses of the implementation:

* Useful extraction rules may be hard to create. While we believe that a number general-purpose rules are widely applicable (string signature, for example, is useful for all kinds of semi-structured string identifiers, such as part numbers, booking references, tracking numbers, social security numbers, etc.), it is true that rules embedding domain-specific knowledge will in general perform better than generic rules (as a side note, since rules are simply Python functions annotated with types, we do not believe that writing rules present technical challenges)
  Taken to the extreme, this is an instance of the following problem: if one wants to write fully accurate validation rules to ensure the consistency of a given dataset, on needs to know exactly what to validate. Using extraction rules instead of boolean functions that return "valid" or "invalid", however, allows users to control the trade-off between accuracy of the outlier detection and amount of domain-specific knowledge fed into the system. In that sense, using extraction rules is a marked progress: significant insight can be extrapolated from little domain-specific knowledge.
  Another convenient aspect of tuple extraction is that the rules tend to be applicable to more than one particular dataset. For this reason, one can imagine building large collections of rules with relatively small application domains, shared among the users of our framework: at modeling time, if these rules do not separate outliers clearly, the expansions that they produce will not be taken into account. Such a collection of rules, collected from users, would in itself be an interesting object of study, and may lead to the elaboration of such meta-rules as suggested by reviewer 1 (interestingly, a very weak notion of such meta-rules is already present in the framework: a single higher-order function is used to generate rules that extract the various bits of an integer value).

* Performance may be an issue, especially on high-dimensional datasets. These issues are of two kinds:
  First, computing expansions may be costly, especially if there are many rules. There are many ways to improve performance (as reviewer 2 points out, efficient data structures could save computations), and fortunately our system is amenable to many optimizations: indeed, since expansion rules are simply python functions, rules can keep some state between invocations. In our current system, it would for example be trivial to add memoization (in fact, thanks to Python's decorator syntax, this could boil down to adding `@memo` in addition to `@rule` before each rule definition). Rule-specific optimizations across tuples are also possible thanks to rule-private state.
  Second, even with optimized expansion rules, the sheer number of expanded tuple fields in high-dimensional datasets may be a problem for performance. In this case, just like models can be trained on a relatively small sample of the data, rules could be selected on a limited sample of the database. This is already implemented in two places: histogram generation, where uninteresting histograms are discarded after processing only a small number of tuples (thus progressively reducing the set of columns for which histograms are built to just a few relevant columns), and correlation detection, where only correlated columns are kept.

We hope that these responses address the main concerns of the reviewers, and we thank them again for the quality of their feedback. Responses to other comments are given below:

> The authors should provide a summary table of the statistical characteristics of the datasets.

Indeed, thanks for pointing out this omission.

> It is unclear exactly how many rules are adopted in the system, and what kind of rules they are. A summary should be provided here.

The current system contains about 20 generally-applicable rules; they are found in https://github.com/cpitclaudel/dBoost/blob/master/dboost/features/__init__.py; we will make sure to add these details to the final version of the paper.

> It is unclear which language and what kind of experiment environment are used. I checked the GitHub repository, and it seems to be Python. This kind of information should be mentioned in the paper.

Indeed, this should be made clearer. The framework consists of about 1000 lines of Python 3 code. Here is the output of pylint on it:

+----------+-------+------+
|type      |number |%     |
+==========+=======+======+
|code      |978    |90.47 |
+----------+-------+------+
|docstring |28     |2.59  |
+----------+-------+------+
|comment   |36     |3.33  |
+----------+-------+------+
|empty     |39     |3.61  |
+----------+-------+------+

> Section IV B -- The section title should be "Data Modeling" instead of "Data modeling".

Thanks!
