import pandas as pd
import numpy as np
import psycopg2
import random
import math
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from statsmodels.tsa.arima_process import ArmaProcess
from numpy.linalg import LinAlgError
from functools import reduce
import warnings
warnings.filterwarnings("ignore")


def arima_range(df, alph, day, i):
    """calculates confidence interval of arima predictions"""
    res = sm.tsa.arma_order_select_ic(df.diff(periods=1)[1:], ic=['aic', 'bic']
                                      , trend='nc')
    (ar, ma) = res.aic_min_order
    try:
        model = ARIMA(df.iloc[(i - int(day * 24 * 12)): i], order=(ar, 1, ma))\
                      .fit(method='css')
        forecast, stderr, conf = model.forecast(steps=int(day * 24 * 12 + 1),
                                                alpha=alph)
        low = conf[int(day * 24 * 12)][0]
        high = conf[int(day * 24 * 12)][1]
        return high, low
    except LinAlgError:
        pass


def reduc(l):
    """calculates returns of all the trades"""
    return reduce(lambda x, y: x * y, [a for (a, b, c) in l]), len(l), l


def next_i(df, i):
    """returns the next i"""
    return df[i: i + 1].values[0]


def get_perc(df, i, num_day, perc):
    """calculates the percentile if a given range"""
    return np.percentile(df[(i - 12 * 24 * num_day): i], perc)


def check_instance(df, bound, i, num_day, perc):
    """if it's a number, divide by 2, else get the percentage"""
    return bound / 2 if isinstance(bound, float) else get_perc(df, i, num_day,
                                                               perc)


def update_bounds(pre, df, i, num_day, perc_high, perc_low):
    """update the trading decision bounds"""
    if (i < 12 * 24 * num_day):
        hbound = get_perc(pre, len(pre), num_day, perc_high)
        lbound = get_perc(pre, len(pre), num_day, perc_low)
    else:
        lbound = get_perc(df, i, num_day, perc_low)
        try:
            hbound, x = arima_range(df, 0.9, num_day, i)
            flag = 0
        except (TypeError, ValueError) as e:
            hbound = get_perc(df, i, num_day, perc_high)
            flag = 1
        if flag == 0:
            hbound = check_instance(df, hbound, i, num_day, perc_high)
        if hbound < lbound:
            hbound = get_perc(df, i, num_day, perc_high)
    return hbound, lbound


res = []


def make_money(df, pre, i=0, n_day=2, perc_hi=80, perc_low=30, bailperc=0.05):
    """run simulation to see the profit potential of given df"""
    if i == len(df) - 1:
        return reduc(res)
    # set bounds
    hbound, lbound = update_bounds(pre, df, i, n_day, perc_hi, perc_low)
    # find the buying point to sell away
    j = 0
    while (i < len(df)) and (next_i(df, i) < hbound):
        i += 1
        j += 1
        if i == len(df) - 1:
            return reduc(res)
        if j > n_day * 12 * 24:
            hbound, lbound = update_bounds(pre, df, i, n_day, perc_hi, perc_low)
            j = 0
    res.append((1 + next_i(df, i), i, 1))
    bail = df[i: i + 1].values[0] + bailperc
    # find the buying point to sell back
    j = 0
    while (i < len(df)) and (next_i(df, i) < bail):
        if df[i: i + 1].values[0] < lbound:
            res.append((1 - next_i(df, i), i, 2))
            make_money(df, pre, i=i)
            return reduc(res)
        i += 1
        j += 1
        if j > n_day * 12 * 24:
            hbound, lbound = update_bounds(pre, df, i, n_day, perc_hi, perc_low)
            j = 0


def create_row(df, start_num, ptile, inday=2, pday=2):
    """create random forest friendly format"""
    tar = df[(start_num + 48 * inputday):(start_num + 48 * (inday + pday))]
    target = tar.quantile(ptile)
    return df[start_num: (start_num + 24 * inputday)], target


def to_fit_rf(df, day=0, perc=0.8):
    """Fit random forest"""
    X, y = [], []
    for i in range(48 * day, 48 * (day + 1)):
        a, b = create_row(df, i, perc)
        X.append(list(a))
        y.append(b)
    y = np.array(y)
    X = np.array(X)
    model = RandomForestRegressor(n_estimators=500, min_samples_split=8,
                                  min_samples_leaf=4, random_state=1)
    model.fit(X, y)
    return model


def to_predict_rf(df, day=1, prec=0.8):
    """predict random forest model"""
    modelu = to_fit_rf(df, day - 1, perc)
    Xpred = []
    for i in range(48 * day, 48 * (day + 1)):
        a, b = create_row(df, i, perc)
        Xpred.append(list(a))
    Xpred = np.array(Xpred)
    high = model.predict(Xpred).mean()
    modeld = to_fit_rf(df, day - 1, 1 - perc)
    Xpred = []
    for i in range(48 * day, 48 * (day + 1)):
        a, b = create_row(df, i, 1 - perc)
        Xpred.append(list(a))
    Xpred = np.array(Xpred)
    low = model.predict(Xpred).mean()
    return high, low
