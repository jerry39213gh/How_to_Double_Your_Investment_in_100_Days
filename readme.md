## Introduction and Project Goal

Cryptocurrency has been a hot topic among the young investors for many months. There is an extremely high ROI in the newly emerged market, but the perceived risk is higher for many who are hesitant to enter the market. To balance the risk and reward, we came up with an arbitrage trading strategy, sacrificing the unreasonably high ROI to limit the exposure risk. Since market inefficiencies still exist in different exchanges, one can take advantage of the spread to do some low risk trading. For example, if Bitcoin is $6,875 USD in market A and $7,000 in a foreign market B today, we can simply buy one Bitcoin in market A and sell it immediately in the foreign market B for a $125 gain. By not keeping the position open, the market risk is significantly reduced. To bring the money back, we can wait until the spread closes or goes the other direction: if Bitcoin is $7,125 in market A and $7,000 in market B 3 days later, we can use the money we have in Korea to buy one Bitcoin, sell it in market A for $7,125 to bring our money back for another gain of $125. The total net gain here is $250, or about 4%, without having to keep the position open. By repeating this process, we doubled our position in 3 months without having to worry about the market risk. The objective of this repo is to demonstrate how we used machine learning algorithms to identify these trading points to maximize the profit.

## Data

The data can be scraped from your choice of cryptocurrency exchanges online, depending on the exchanges you want to work with. The price spread can be calcualted by dividing the price of exchange A by exchange B. An example of the price differentials between the US and Korea in September of last year can be found ![here](https://github.com/jerry39213gh/How_to_Double_Your_Investment_in_100_Days/blob/master/main.csv). To give you a sense of what the algorithm is doing, ![here](https://github.com/jerry39213gh/How_to_Double_Your_Investment_in_100_Days/blob/master/illustration.pdf) is an illustration of the algorithm in action. The red dots represent the action point to buy in the US and sell in Korea, and the green dots are the opposite. The y axis "spread" can be read as "the price of Bitcoin in Korea is currently x% more expensive than that of the US". Basically, we want the preceding red dots to be higher than the green dots. Using the data shared in this repo, the algorithm generated a 33% gain after 22 trade rounds in September, and a little under 100% during the last quarter of 2017. 

### Please note:
  
- The calculations here do not take transaction fees into consideration. While the transaction fees are fairly negligible for some exchanges, they can be significant for others. It is important to take this into consideration when you are shopping for the right exchanges to work with. The simulation with transaction fees included reduces the gains by about 5% per month.   
- The calculations here assume the transactions are immediate, which is not the case in real life. However, the transcations for the exchanges we are working with usually only takes 10-15 minutes, so it's not a big concern.
- Even though we are using Bitcoin as an example for this repo, the strategy works for other coins as well. Transaction times and trading volumes vary depending on your choice of coin and your choice of exchange. Keep in mind that exchanges with low volumes are more prone to slippage.
- The calculations here do not take bid-ask spread into consideration. The spread between exchanges are typically a lot higher, so this is not really an issue.   
- As of late November when Bitcoin hit $10,000, the crypto craze has generated so much noise that it has become harder to predict the pattern of the spread. Minor modifications and more human judgment are needed to maximize the gains until the pattern stablizes again.

## Model Selection, Validation, and Parameter Tuning

Random forest and ARIMA were selected since the preliminary results were proven to be promising. 

### The decision algorithm:

If the spread hits A% (high), buy from market A and sell to market B.
When the spread comes back down to B% (low), buy from market A and sell to market B.
Update the new high and low based on previous patterns using ARIMA and RF. Then repeat the loop.

If no trades are made for 2 days, update the new high and low and reset the algorithm.
If a trade is made at A% (high) and the spread goes up for another 5%, bail and take the loss, wait until the pattern stabilizes again, update the high and low and reset the algorithm.

### Other notes

Different models can identify different trading opportunities. For example, the Random Forest algorithm identifed a few additional opportunities between 9/5 - 9/7 and between 9/24 - 9/26 when the ARIMA algorithm was idle. Combining multiple models together can improve the trading results (code not shown in this repo). 

### ARIMA

The data was decomposed to check for trend and seasonality, but no patterns were observed. This made sense as we would expect the prices from the two markets to be moving somewhat together, making the spread relatively stable. With that, we decided to use the data assuming no trend or seasonality. The first differences were then taken to create a new series. Box Cox test was used to show that the series was homoscedastic, and Dickey Fuller test was used to show that the series was stationary. Using the combination of ACF plot, PACF plot, and auto select ARIMA, the final candidate model was selected. With the ARIMA selected model, we can feed in 2 days of data to predict 2 days ahead, and use the confidence intervals to determine our trading targets.

### Random Forest

Take 2 days of data to predict the range of the movement in the next 2 days with 500 trees and a few other specifications. The random forest algorithm doens't seem to work as well as ARIMA, but is a good model to complement the base model to identify additional opportunities.

## Model Validation

The individual models were first validated using the usual time series "ladder" break down using 4 folds of the August data. The individual models were tuned using the accuracy of the predictions, then the decision algorithm was tuned using the highest return of the August data. The data in September was going to be the test set, but the algorithm was implemented early due to the high opportunity cost. We did not implement the Random Forest algorithm in September, but played around with it and decided to add it to aid our trading decision in October. The model fitting steps were not as rigorous as we'd like to, but post hoc analysese showed that the parameters we selected worked pretty well for the following months.       

## Future Directions

As mentioned above, recursive models may give more accurate predictions of the results.  We can also consider ensembling the models in other ways to improve the results. Considering that the opportunity may not be around forever and the current model is good enough, no further actions will be taken at the moment.

## Acknowledgment

- Jesse wrote this document and was responsible for handling the data and creating the algorithms
- John set up the trading platforms and built the trading bot (code not included in this repo)  
