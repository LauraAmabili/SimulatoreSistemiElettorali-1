import pandas as pd


def relative_column(serie):
    s = serie.sum()
    return serie / s


def concat(*dfs):
    return pd.concat(dfs)