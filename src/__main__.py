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
import io
from multiprocessing import Pool
import pandas
import yaml
import os
import inspect, importlib
import sys
from src.Metaclasses import *
from src import Commons
import argparse  # Usa per avere in input i
import src

parser = argparse.ArgumentParser(
    description='This program uses the configuration files and data provided to simulate an '
                'electoral process')
parser.add_argument('path', help='the path to the directory containing the configuration files', nargs='*')

if __name__ == '__main__':
    args = parser.parse_args()
    f = open("logs", 'w')
    save_stdout = sys.stdout
    sys.stdout = f
    for i in args.path:
        res = src.run_simulation(i)
    sys.stdout = save_stdout
    f.close()

    print(res)


