#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
eps = 0.0000001

def signal(*args):
    # Acs 指标
    df = args[0]
    n = args[1]
    factor_name = args[3]
    df['pct'] = df['close'].pct_change()
    df['pct_max'] = df['pct'].rolling(n).max()
    df[factor_name] = df['pct_max']

    return df
def get_parameter():
    param_list = []
    n_list = range(10,100,10)
    for n in n_list:
        param_list.append(n)

    return param_list
