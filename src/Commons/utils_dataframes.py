import pandas as pd


def relative_column(serie):
    s = serie.sum()
    return serie / s


def concat(*dfs):
    return pd.concat(dfs)


def fill_column(data, column, column_val):

    df = data.copy()
    df[column] = column_val

    return df