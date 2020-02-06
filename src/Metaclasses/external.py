from copy import deepcopy
import pandas as pd
import src.utils
import src.GlobalVars
from src import Commons
commons = Commons

class external(type):
    """
    Has to be amongst the last ones to be called

    Parses configurations of the type:
        +

    """

    def __new__(mcs, *args, external=None, **kwargs):
        if external is None:
            external_data = []
        else:
            external_data = external

        print("External conf: ", external_data)

        init_vars = [(k, d.get('default', ())) for k, d in external_data.items()
                     if (type(d) == dict) and (d.get('init', False))]
        print("Init vars external: ", init_vars)

        o_init = args[2].get('__init__', lambda *s, **k: None)

        def __init__(self, *args_in, **kwargs_in):
            print("Init operations of external: ")
            for i, default in init_vars:
                prov = getattr(self, f'give_{i}')
                if default == ():
                    prov(kwargs_in.pop(i))
                else:
                    prov(kwargs_in.pop(i, default))

            return o_init(self, *args_in, **kwargs_in)

        args[2]['__init__'] = __init__

        accessors = mcs.gen_accessors(external_data)
        args[2].update(accessors)

        providers = mcs.gen_providers(external_data)
        args[2].update(providers)

        print("external processed: ", external_data)
        print(accessors, providers)

        return super().__new__(mcs, *args, **kwargs)

    @staticmethod
    def parse_conf(conf):
        return conf

    @staticmethod
    def gen_accessors(conf):

        def gen_fun(var):
            source, nome, cols, typ = var
            col_l, col_d = src.utils.parse_columns(cols)

            def acc(self):
                s = getattr(self, source)
                if len(col_l) == 0:
                    if typ == "int":
                        return int(s)

                    if typ == "float":
                        return float(s)

                    if typ is not None:
                        print(dir(src.GlobalVars))
                        return src.GlobalVars.Hub.get_instance(typ, s)

                    return deepcopy(s)

                else:  # s is a dataframe
                    if type(s) != pd.DataFrame:
                        raise TypeError("Not a dataframe but provided columns")
                    return s[col_l].rename(columns=col_d).copy()

            return nome, acc

        lis_names = []  # sorgente, nome, colonne

        for k, d in conf.items():  # k è la sorgente
            if type(d) != dict:
                d = dict()
            if 'targets' in d:  # più output
                for i in d['targets']:  # ogni i è un dizionario
                    lis_names.append((k, i['name'], i.get('columns', []), None))
            else:  # stesso nome o primo livello
                lis_names.append((k, d.get('name', k), d.get('columns', []), d.get("type", None)))

        m = map(gen_fun, lis_names)
        fs = {}
        for i, f in m:
            fs[f'get_{i}'] = f
        return fs

    @staticmethod
    def gen_providers(conf):
        conf = deepcopy(conf)

        lis_f = conf.keys()

        def gen_fun(var):
            def give(self, val):
                print("Adding ", val, " come ", var)
                setattr(self, var, val)

            return var, give

        m = map(gen_fun, lis_f)
        fs = {}
        for i, f in m:
            fs[f'give_{i}'] = f
        return fs
