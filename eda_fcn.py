from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def auto_fcn_plot(df, lags):
    """Plots acf and pacf functions of the df and number of lags given"""
    fig = plt.figure(figsize=(15, 8))
    axa = fig.add_subplot(211)
    axa.set_ylim([-0.075, 0.075])
    fig = plot_acf(df, lags=lags, ax=axa)
    axb = fig.add_subplot(212)
    axb.set_ylim([-0.075, 0.075])
    fig = plot_pacf(df, lags=lags, ax=axb)
    plt.show()
    return


def stationary_test(df):
    """Test whether the given series is stationary"""
    rollmean = pd.rolling_mean(df, window=12)
    rollstd = pd.rolling_std(df, window=12)
    origin = plt.plot(df, c='b', label='Original')
    mean = plt.plot(rollmean, c='r', label='Rolling Mean')
    std = plt.plot(rollstd, c='g', label='Rolling Std')
    plt.legend()
    plt.title('Rolling Mean & STD')
    plt.show()

    dfad = adfuller(df, autolag='AIC')
    output = pd.Series(dfad[0:4], index=['stats', 'pval', '#lags', 'nobs'])
    for key, value in dfad[4].items():
        output['Critical Value (%s)' % key] = value
    print(output)


def decompose(df):
    """decompose and plot df into seasonal, trend, and residuals"""
    decomposition = seasonal_decompose(df, freq=2016)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(df, label='df', figsize=(20, 5))
    plt.legend()
    plt.subplot(412)
    plt.plot(trend, label='df_trend', figsize=(20, 5))
    plt.legend()
    plt.subplot(413)
    plt.plot(seasonal, label='df_season', figsize=(20, 5))
    plt.legend()
    plt.subplot(414)
    plt.plot(residual, label='df_residuals', figsize=(20, 5))
    plt.legend()
    plt.show()
    return


def create_row(df, start_num, ptile, inputday=2, predday=2):
    """Function used to make time series data random forest friendly"""
    target = df[(start_num + 48 * inputday):(start_num + 48 * (inputday +
                predday))].quantile(ptile)
    return series[start_num: (start_num + 24 * inputday)], target
