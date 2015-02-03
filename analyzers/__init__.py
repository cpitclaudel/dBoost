def ALL():
    from . import statistical, discrete
    return (statistical.Pearson, discrete.DiscreteStats)
