from pandas import DataFrame
import numpy as np
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta
from freqtrade.strategy.interface import IStrategy
import freqtrade.vendor.qtpylib.indicators as qtpylib

#https://in.tradingview.com/script/32ZHCA6S-QuantNomad-RSI-Strategy-NKE-5m/
#https://in.tradingview.com/script/f7F71vdS-QuantNomad-RSI-Strategy-LTCUSDT-5m/

parame ={
"length" : 10,
"overSold" : 40, 
"overBought" : 60, 
}

class new_strategy(IStrategy):

    minimal_roi = {
    "170": 0.01,
    "40": 0.01,
    "30": 0.03,
    "20": 0.02,
    "0": 0.01
    }
  
    stoploss = -0.08
    ticker_interval = "5m"
    use_sell_signal = True
    sell_profit_only = True
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.011

    def get_ticker_indicator(self):
      return int(ticker_interval[:-1])

    def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
        #Bollinger-Band
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=24, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        #RSI
        dataframe['vrsi'] = ta.RSI(dataframe, parame['length'], price ='close')
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
              dataframe.loc[
                  (

                      ((dataframe['vrsi'] > parame['overSold']) & (dataframe['vrsi'] < parame['overBought'])) & (dataframe['close'] < dataframe['bb_lowerband'])


                  ),
                  'buy'] = 1
              return dataframe
    def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
              dataframe.loc[
                  (
                       (dataframe['close']  > dataframe['bb_upperband'])
                  ),
                  'sell'] = 1
              return dataframe
