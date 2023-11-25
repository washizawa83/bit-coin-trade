import pandas as pd

from indicators.trend import Trend
from indicators.max_min_price import MaxMin
from finance.finance import Candle


class ParabolicSAR:
    step = 0.02
    maximum = 0.2

    def __init__(self, sar: pd.DataFrame, trend: Trend, price) -> None:
        self._sar = sar
        self._current_trend = trend
        self._updated_price = price
        self._current_step = 0.02

    # SAR = 前足のSAR + AF * (EP - 前足のSAR)
    def _calc_sar(self):
        prev_sar = self._sar.iloc[-1]['Sar']
        return prev_sar + self.step * (self._updated_price - prev_sar)

    def _convert_sar(self, current_candle):
        self._sar = pd.concat([self._sar, pd.DataFrame.from_dict(
            {current_candle.name: [self._updated_price]},
            orient='index',
            columns=['Sar']
        )])
        if self._current_trend.is_up_trend():
            self._updated_price = current_candle['Low']
        else:
            self._updated_price = current_candle['High']
        self._current_trend = Trend(
            current_candle.name, not self._current_trend.is_up_trend())
        self._current_step = self.step

    def _concat_sar(self, current_candle):
        new_sar = {current_candle.name: [self._calc_sar()]}
        self._sar = pd.concat([self._sar, pd.DataFrame.from_dict(
            new_sar,
            orient='index',
            columns=['Sar']
        )])

    @classmethod
    def create_sar(cls, candle: Candle, max_min: MaxMin, trend: Trend):
        prevent_sar = max_min.get_max_min().iloc[-1]
        current_candle = candle.get_all_candles().iloc[-2]
        sar_dataframe = pd.DataFrame(
            {'Sar': prevent_sar['Price']}, index=[current_candle.name])
        sar_dataframe.index.name = 'Date'
        updated_price = 0
        if trend.is_up_trend():
            updated_price = current_candle['High']
        else:
            updated_price = current_candle['Low']
        return cls(sar_dataframe, trend, updated_price)

    def update_sar(self, candle: Candle):
        # 上昇トレンド
        if self._current_trend.is_up_trend():
            current_candle = candle.get_all_candles().iloc[-2]
            # 転換した場合
            if current_candle['Low'] < self._sar.iloc[-1]['Sar']:
                self._convert_sar(current_candle)
                return

            if self._updated_price < current_candle['High']:
                self._updated_price = current_candle['High']
                self._current_step = self._current_step if self.maximum <= self._current_step else self._current_step + self.step

            self._concat_sar(current_candle)
        # 下降トレンド
        else:
            current_candle = candle.get_all_candles().iloc[-2]
            # 転換した場合
            if self._sar.iloc[-1]['Sar'] < current_candle['High']:
                self._convert_sar(current_candle)
                return

            if current_candle['Low'] < self._updated_price:
                self._updated_price = current_candle['Low']
                self._current_step = self._current_step if self.maximum <= self._current_step else self._current_step + self.step

            self._concat_sar(current_candle)

    def get_all_sar(self):
        return self._sar
