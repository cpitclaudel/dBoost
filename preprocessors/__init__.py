def ALL():
    from . import statistical
    from . import discrete 
    from . import cords 
    return (statistical.Pearson, discrete.DiscreteStats)
