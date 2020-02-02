# -*- coding: utf-8 -*-
import copy
import functools

import pandas as pd

import src.GlobalVars
import src.utils
from src.utils import *

class totals(type):
    
    """
    Proper totals accept:
        + self
        + type
        + *filters
    """
    def __new__(mcs, *args, totals, **kwargs):
        for name, config in totals.items():
            pass

        return super().__new__(mcs, *args, **kwargs)

    @classmethod
    def parse_aggregate(mcs, totals=True, *, keys, source, ops, **kwargs):
        """
        keys: Le colonne comuni, lista di stringhe
        Source: una funzione che restituisce un dataframe con chiavi ripetute, gli serve locals()
        Ops: le operazioni da eseguire su ogni colonna, un dizionario con chiavi le colonne e valori:
            - str in [mean, median, prod, sum]
            - str che è una funzione runnare con eval()

        Generates a function which accepts:
            + self
            + *sbarramenti
        """
        ops_f = {}
        for k, op in ops.items():
            if op in ['mean', 'median', 'sum', 'prod']:
                ops_f[k] = op
            else:
                ops_f[k] = eval(op)

        if totals:
            def aggregate_totals(locs, *sbarramenti, **kwargs):
                df = source(locs, *sbarramenti, **kwargs)
                return df.groupby(keys).agg(ops_f).reset_index()

            return aggregate_totals

        def aggregate_support(locs, *args, **kwargs):
            df = source(locs, **kwargs)
            r = df.groupby(keys).agg(ops_f)
            return r.reset_index()

        return aggregate_support

    @classmethod
    def parse_transform_op_df(mcs, source, **kwargs):
        """
        The function applying a function to the whole dataframe

        Source è una funzione a cui passare il dataframe come data=df
        """

        def whole_df_transform(locs, df):
            return source(locs, data=df)

        return whole_df_transform

    @classmethod
    def parse_transform_op_col(mcs, *, source, replace_name=None, column, column_type=None, **kwargs):
        """
        The function applying a function to every cell of an individual column, either creating a new column value or
        replacing a previous one

        Source è una funzione, ci passo data=df

        Se replace_name non è None allora il risultato finisce in una colonna

        column indica il nome della colonna
        column_type indica il tipo della colonna
        """

        def column_transform(locs, df):
            """

            """
            col = df[column]
            if column_type is not None:
                col = src.utils.transform_column(col, column_type)

            def act_on_cell(cell):
                return source(locs, cell)

            res_col = col.map(act_on_cell)

            df_r = df.copy()

            if replace_name is not None:
                df_r[replace_name] = res_col
            else:
                df_r[column] = res_col
            return df_r

        return column_transform

    @classmethod
    def parse_transform_op_lin(mcs, source, column_name, **kwargs):
        """
        The function taking each row and returning a column value, it calls a function using each row as a dict
        """

        def row_transform(locs, df):
            def applied(row):
                dic = row.to_dict()
                return source(locs, **dic)

            df2 = df.copy()
            df2[column_name] = df.apply(applied, axis=1)

            return df2

        return row_transform

    @classmethod
    def parse_transform(mcs, totals=True, *, source, ops, **kwargs):
        """
        ops è una lista di dizionari, ogni dizionario definisce una trasformazione, i risultati devono essere incatenati
        source è una funzione che restituisce il df da cui partire
        """

        ops_a = []
        for i in ops:
            """
            Ogni elemento di ops è un dizionario con almeno la chiave "type"
            """
            if i['type'] == "column":
                ops_a.append(mcs.parse_transform_op_col(**i))
            elif i['type'] == "line":
                ops_a.append(mcs.parse_transform_op_lin(**i))
            elif i['type'] == "dataframe":
                ops_a.append(mcs.parse_transform_op_df(**i))
            else:
                raise TypeError("Unrecognized transform operation type")
        ops = ops_a
        def apply_ops(locs, first_df):
            df = first_df
            for i in ops:
                df = i(locs, df)
            return df

        if totals:
            def transform_totals(locs, *sbarramenti, **kwargs):
                df = source(locs, *sbarramenti, **kwargs)
                return apply_ops(locs, df)
            return transform_totals
        else:
            def transform_support(locs, *oth, **kwargs):
                df = source(locs, **kwargs)
                return apply_ops(locs, df)
            return transform_support

    @classmethod
    def parse_combination(mcs, totals=True, *, function, keys, args, **kwargs):
        """
        Se totals è true allora alle funzioni sotto passa gli sbarramenti altrimenti no

        function: stringa
        keys: le chiavi da usare per fare merge dei dataframe e per aggregare
        args: una lista. Gli elementi della lista possono essere:
            + literal
            + dizionario con solo due chiavi: "type" che può essere "series", "dataframe" or "scalar" e "source" che è una
                funzione
        """

        fun = eval(function, globals(), locals())

        def fun_from_scalar(i):
            def f(*a,**k):
                return i
            return f

        dataframes = [] #
        series = []
        scalars = []

        for i in args:
            if type(i) != dict:
                scalars.append(fun_from_scalar(i))
            elif i.get('type') == 'series':
                series.append(i.get('source'))
            elif i.get('type') == 'dataframe':
                dataframes.append(i.get('source'))
            else:
                scalars.append(i.get('source'))

        def ops(dfs, ses, scs):
            if len(dfs) > 1:
                frame = functools.reduce(lambda a, b: pd.merge(a, b, on=list(keys)), dfs)
            else:
                frame = dfs[0]
            gps = frame.groupby(list(keys))
            res = []
            for g, f in gps:
                g = list(g)
                fun_kw = {}
                for ser in ses:
                    m = [ser[keys[i]] == g[i] for i in range(len(g))]
                    fil = m[0]
                    for i in m[1:]:
                        fil = fil & i
                    kw_l = dict(ser[fil].iloc[0])
                    for i in keys:
                        kw_l.pop(i, None)

                    fun_kw.update(kw_l)
                res.append(fun(f, *scs, **fun_kw))
            return pd.concat(res, ignore_index=True)

        if totals:
            def comb_totals(locs, *sbarramenti, **kwargs):
                act_dataframes = [i(locs, *sbarramenti, **kwargs) for i in dataframes]
                act_series     = [i(locs, *sbarramenti, **kwargs) for i in dataframes]
                act_scalars    = [i(locs, *sbarramenti, **kwargs) for i in scalars]
                return ops(act_dataframes, act_series, act_scalars)

            return comb_totals

        def comb_support(locs, *args, **kwargs):
            act_dataframes = [i(locs, **kwargs) for i in dataframes]
            act_series = [i(locs, **kwargs) for i in dataframes]
            act_scalars = [i(locs, **kwargs) for i in scalars]

            return ops(act_dataframes, act_series, act_scalars)

        return comb_support

    @classmethod
    def parse_multi(mcs, **kwargs):
        """
        Se totals è true allora alle funzioni sotto passa gli sbarramenti altrimenti no
        """
        if totals:
            def multi_totals(locs, *sbarramenti, **kwargs):
                pass

            return multi_totals

        def multi_support(locs, *args, **kwargs):
            pass

        return multi_support

    @classmethod
    def parse_total_proper(mcs, tot_name, **kwargs):
        """
        Chiama parse_total_support con totals=True
        """
        f = mcs.parse_total_support(True, **kwargs) # funzione che accetta locals, *args e **kwargs

        def totals(self, type, *sbarramenti, **kwargs):
            res = f(locals(), *sbarramenti, **kwargs)

            columns = res.columns()
            def apply_filter(row):
                polEnt = src.GlobalVars.Hub.get_instance("PolEnt", row[columns[0]])
                return polEnt.filter(self, type, row, res)

            return res[res.apply(apply_filter, axis=1)]

        return tot_name, totals

    @classmethod
    def parse_total_support(mcs, totals=False, *, rename=None, columns=None, type,  **kwargs):
        """
        Chiama il parser appropriato collegando totals
        """
        if rename is None:
            rename = {}
        if columns is None:
            columns = []
        
        cols, ren_cols = parse_columns(columns)
        if len(cols) > 0:
            restrict = True
            rename.update(ren_cols)

        def totals_support(self, *args, **kwargs):
            pass

        return totals_support

    @classmethod
    def parse_conf(mcs, configuration):
        if type(configuration) == list:
            return list(map(mcs.parse_conf, configuration))
        if type(configuration) != dict:
            return configuration
        if 'source' not in configuration:
            return {k: mcs.parse_conf(v) for k, v in configuration.items()}

        source = configuration['source']
        new_source = {}
        for k, v in source.items():
            if k == "totals":
                new_source['type'] = 'fun'
                new_source['name'] = 'self.totals'
                new_source['args'] = [v] + source.get('args', [])
            else:
                new_source[k] = mcs.parse_conf(v)

        for k, v in configuration.items():
            if k == 'source':
                configuration[k] = new_source
            else:
                configuration[k] = mcs.parse_conf(v)

        return configuration
