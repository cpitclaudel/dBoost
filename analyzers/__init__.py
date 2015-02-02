def ALL():
    from . import statistical, discrete, cords
    return (statistical.Pearson, discrete.DiscreteStats, cords.Cords)
