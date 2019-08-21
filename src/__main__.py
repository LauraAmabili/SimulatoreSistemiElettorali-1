# -*- coding: utf8 -*-
"""
This is the main file of the project, it will be called providing the necessary configuration
files:
+ Structure config (regional divisions as well as political divisions), will be used to create the classes
+ Structure declaration, will create the instances of the physical divisions
+ Data:
    - For the physical layer it will provide the data to the "data sources"
    - For the political layer it'll declare membership of parties into coalitions, candidates in parties and
    candidates or parties in the appropiate position related to candidacy in physical division

Permette di eseguirlo come python -m src
"""
import yaml
import os
import inspect, importlib
import sys
import src
import src.Metaclasses
import src.Commons
from src.Simulator import ClassBuilder
import argparse # Usa per avere in input i

parser = argparse.ArgumentParser(description='This program uses the configuration files and data provided to simulate an '
                                             'electoral process')
parser.add_argument('path', help='the path to the directory containing the configuration files', nargs='*')
args = parser.parse_args()
files = [os.path.join(dirpath, filename)
    for i in args.path
    for (dirpath, dirs, files) in os.walk(i)
    for filename in (dirs + files)]

dict_metas = { k:getattr(src.Metaclasses,k) for k in filter(lambda x: x[:2]!="__", dir(src.Metaclasses)) }

path_cust_meta = os.path.join(args.path[0], 'Metaclasses')
if os.path.isdir(path_cust_meta):
    for fname in filter(lambda x: x[-3:]=='.py', next(os.walk(path_cust_meta))[2]):
        fpath = os.path.join(path_cust_meta, fname)
        spec = importlib.util.spec_from_file_location(fname[:-3], fpath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)

        class_name = list(filter(lambda x: x[:2] != "__", dir(foo)))

        for i in class_name:
            classe = getattr(foo, i)
            if issubclass(classe, type):
                print('custom ',classe)
                dict_metas[classe.__name__] = classe

dict_commons = { k:getattr(src.Commons,k) for k in filter(lambda x: x[:2]!="__", dir(src.Commons)) }

path_cust_comm = os.path.join(args.path[0], 'Commons')
if os.path.isdir(path_cust_comm):
    for fname in filter(lambda x: x[-3:]=='.py', next(os.walk(path_cust_comm))[2]):
        fpath = os.path.join(path_cust_comm, fname)
        spec = importlib.util.spec_from_file_location(fname[:-3], fpath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)

        class_name = list(filter(lambda x: x[:2] != "__", dir(foo)))

        for i in class_name:
            classe = getattr(foo, i)
            if inspect.isclass(classe) or inspect.isfunction(classe):
                dict_metas[classe.__name__] = classe

cdfs = list(filter(lambda x: x[-4:]=='.cdf', files))
dict_classi = dict()
for i in cdfs:
    with open(i,'r') as f:
        d_l = yaml.safe_load(f)
        for k in d_l:
            dict_classi[k] = d_l[k]
hub = ClassBuilder.HubBuilder.buildHub(dict_classi, dict_metas, dict_commons)

idfs = list(filter(lambda x: x[-4:]=='.idf', files))
csvs = list(filter(lambda x: x[-4:]=='.csv', files))
