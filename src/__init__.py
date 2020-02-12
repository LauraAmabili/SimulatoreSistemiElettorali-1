import src.GlobalVars
from runpy import run_path
import sys
import pandas as pd
import src
import os
from src.Metaclasses import *
import src.GlobalVars as GlobalVars
import yaml

from src import Commons
commons = Commons


def run_simulation(path):
    src.GlobalVars.Hub = src.GlobalVars.ActHub()
    base_path = path
    classes = next(os.walk(os.path.join(base_path, 'Classes')))
    for i in classes[2]:
        pth = os.path.join(base_path, 'Classes', i)
        name = i.split('.')[0]

        if '.py' in i:
            d = run_path(pth, globals())
            exec(f"{name} = d['{name}']")
        elif '.yaml' in i:
            with open(pth, 'r') as f:
                conf = yaml.safe_load(f)
            metas = [eval(i) for i in conf.pop('metaclasses')]
            for i in metas:
                conf = i.parse_conf(conf)

            conf = sources_parse.source_parse(conf)
            metas_f = tuple(metas + [cleanup])
            comb = type(f'comb_{name}', metas_f, {})

            c = comb(name, (), {}, **conf)
            exec(f'{name}=c')

    # -------
    instances = next(os.walk(os.path.join(base_path, 'Instances')))
    for i in instances[2]:
        print(i)
        cls = eval(i.split('.')[0])
        with open(os.path.join(base_path, 'Instances', i), 'r') as f:
            d = yaml.safe_load(f)
            for k, conf in d.items():
                print(k)
                cls(k, **conf)

    data = next(os.walk(os.path.join(base_path, 'Data')))
    for f in data[1]:
        path = os.path.join(base_path, 'Data', f)
        for csv in next(os.walk(path))[2]:
            name = csv.split('.')[0]
            df = pd.read_csv(os.path.join(path, csv))
            for k, data in df.groupby(df.columns[0]):
                r = GlobalVars.Hub.get_instance(f, k)
                getattr(r, f'give_{name}')(data.iloc[:, 1:])

    return src.GlobalVars.Hub.run_exec()