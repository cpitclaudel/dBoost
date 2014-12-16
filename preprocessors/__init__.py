def ALL():
    from . import statistical
    from . import discrete 
    return (statistical.Pearson, discrete.DiscreteStats)
