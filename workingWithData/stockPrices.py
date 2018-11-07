from __future__ import division
from collections import Counter
from matplotlib import pyplot as plt
import functions as fnc
import math, random

import dateutil.parser, csv

def parse_row(input_row, parsers):
    """apply appropriate pareser to each element in input row"""
    return [try_or_none(parser)(value) if parser is not None else value
            for value, parser in zip(input_row, parsers)]

def parse_rows_with(reader, parsers):
    """wrap a reader to apply parers to each of its rows"""
    for row in reader:
        yield parse_row(row,parsers)

def try_or_none(f):
    """wraps f to return none if f raises exception, assumes f only takes one input"""
    def f_or_none(x):
        try: return f(x)
        except: return None
    return f_or_none

data = []

with open("comma_delimited_stock_prices.csv","rb") as f:
    reader = csv.reader(f)
    for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
        data.append(line)

for row in data:
    if any(x is None for x in row):
        print row
