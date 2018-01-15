from main_fcn import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    df = pd.read_csv('main.csv')
    pre = pd.read_csv('pre.csv')
    df.set_index('created_at', inplace=True)
    pre.set_index('created_at', inplace=True)
    df = df['arbitrage']
    pre = pre['arbitrage']
    res = []
    (gain, num_trades, res) = make_money(df, pre)
    print('The gain is', gain, "after", num_trades, "trades.")
    tradein = [time for (prec_gain, time, in_out) in res if in_out == 1]
    tradeout = [time for (prec_gain, time, in_out) in res if in_out == 2]

    df.plot(figsize=(20, 5), c='y', alpha=0.5)
    x = np.array(tradein)
    y = df[x]
    inn = plt.scatter(x, y, c='r')
    xo = np.array(tradeout)
    yo = df[xo]
    out = plt.scatter(xo, yo, c='g')
    plt.legend((inn, out), ('Trade In', 'Trade Out'))
    plt.suptitle('Trading Algorithm in Action')
    plt.xlabel('Date')
    plt.ylabel('Spread')
    plt.show()
