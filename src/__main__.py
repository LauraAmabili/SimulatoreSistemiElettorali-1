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
import sys
import src
import src.Metaclasses
import src.Commons
import argparse # Usa per avere in input i

print("Hey")
