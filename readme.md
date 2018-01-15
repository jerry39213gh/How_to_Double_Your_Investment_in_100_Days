Introduction and Project Goal

Cryptocurrency has been a hot topic among the young techies for many months. There is an extremely high return of investment in the newly emerged market, but the perceived risk is higher for many who are hesitant to enter the market. To balance the risk and reward, we came up with an arbitrage trading strategy, sacrificing the unreasonably high ROI to limit the exposure risk. Since market inefficiencies still exist in different exchanges, one can take advantage of the spread to do some low risk trading. For example, if BitCoin is $6,500 USD in market A and $7,000 in a foreign market B today, we can simply buy one BitCoin in market A and sell it immediately in the foreign market B. By not keeping the position open, the risk is significantly reduced. One problem here is that the money will be stuck in market B's local fiat currency. To bring the money back, we would have to wait until the spread closes a little. For example, say 3 days later BitCoin is $6,750 in market A and $7,000 in market B, we can then use the money we have that's sitting in market B to buy one BitCoin, and sell it in market A for $6,500. The total net gain here is $250, or about 4%, without having you keep your position open and expose yourself to the high volatility. If we were to make a trade like this every few days, we can easily double our current position in 3 months and have very limited risk exposure to the market. Now, we need to identify the high points and the low points in our spread to maximize our return- imagine buying 1.045 and selling at 1.005 for a sine-wave like pattern that oscillates between 1.00 and 1.05. The objective of this project is to use machine learning algorithms to identify these points.

Data

The data can be scraped from your choice of cryptocurrency exchanges online, depending on which ones you want to work with. By dividing the price of exchange A by exchange B, we can get the percentage difference of the going price of your choice of cryptocurrency. Below is an example of the time series data from September.    

![alt text](https://github.com/jerry39213gh/How_to_Double_Your_Investment_in_100_Days/blob/master/illustration.pdf)


Please note:

- Even if we make a mistake trade at 1.01 and the spread keeps going up afterwards, we can just wait until the spread comes back down to 1.00 to trade back. While we are not going to lose money from the trade, a mistake trade like that will reduce the number of trades we can make, in turn reducing the total return. A "stop loss" rule can be implemented here to take a small loss in exchange for a higher number of trades.     
- The calculations here do not take transaction fees into consideration. Granted, the fees are relatively negligible considering that the spread can be quite high.
- The calculations here do not take the transaction time into consideration, but the price spread usually doesn't slip too much in 10-15 minutes, so it's not a huge concern.
- While we are talking about slippage and trading time, you should carefully pick the coins you want to use for the trading strategy. Transaction times vary depending on your choice of coin and your choice of exchange. Some takes longer than others. Some coins also have a lower trading volume on certain exchanges and are more prone to slippage, so you should take that into consideration as well.
- The calculations here do not take bid-ask spread into consideration. The spread between exchanges are typically a lot higher, so this is not really an issue.
- The algorithm structure shown here is being used in a live trading app. That portion of the code is not available in this repo.   
- As of late November when BitCoin hit $10,000, the crypto craze has generated so much noise that it became harder to predict the pattern of the spread. Minor modifications and more human judgment will be needed to maximize the gains until the pattern stablizes again. In the meantime, you can still easily get a 20%-30% monthly return if you know what you are doing.   

Model Selection, Validation, and Parameter Tuning

Random forest and ARIMA are selected for the model since they're relatively simple to implement and the preliminary results were proven to be promising. Recurrent neural networks may be added once I get a better grasp of the topic. Other recursive models may also be considered.

The decision algorithm:

If the spread hits A% (high), buy from market X and sell to market Y.
When the spread comes back down to B% (low), buy from market Y and sell to market X.
Update the new high and low based on previous patterns using ARIMA and RF. Then repeat the loop.

Exceptions:

If no trades are made for 3 *note to self: grid search this number* days, update the new high and low and reset the algorithm.
If a trade is made at A% (high) and the spread goes up for another 5% *note to self: grid search this number*, bail and take the loss, wait until the pattern stabilizes again, update the high and low and reset the algorithm.  

ARIMA:

The data was decomposed to check for trend and seasonality, but no pattern was observed. This makes sense as I would expect the prices from the two markets to be moving somewhat together, making the spread relatively stable. With that, I decided to use the data as is to proceed. The first difference is then taken to create a new series. Box Cox test was used to show that the series is homoscedastic *include p value*, and Dickey Fuller test was used to show that the series is stationary *include p value*. Using the conjunction of ACF plot, PACF plot, and auto select ARIMA, the final candidate was selected to be ARIMA(3,1,2) *grid test this as well*. With our ARIMA model, we can feed in *test* days of data to predict *test* days ahead, using *test*% confidence interval to find the upper bound and the lower bound as out trading targets. *also tune the tree parameters*

Random Forest:

Take *test* days of data to predict the range (low,high) of the movement in the next *test* days with *test* number of trees *and tune other parameters*.

Validation and Result

The September data was broken down 75% 25% in the usual time series 4 fold cross validation way, using the most recent quarter as the validation data and the rest as the training data. The top candidate was implemented immediately since there's money to be made without a possible loss, but the top 3 scoring candidates were run in parallel as an ad hoc test set to select the top performing model. Technically, a multi-armed bandit approach could be used here to further optimize the result, but it was ruled out due to the extra effort of implementation. *update results*    

Future Directions:

As I mentioned above, recursive models may give more accurate predictions of the results.  We can also consider ensembling. A few strategies:

1. Random forest and ARIMA both output a lower bound and a upper bound (trading points). Use a linear combination to determine the optimal output.
2. We can use a multi-layered model. That is, use random forest to find the confidence interval, and use ARIMA to predict the whether the trend is going up or down at our trading points. We can potentially get another half a percent in for each trade that way.

*will try both*
