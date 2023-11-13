from typing import Optional
import pandas as pd

from indicators.sma import Sma


class Trend:
    def __init__(self, change_trend_date: str, is_up_trend: bool) -> None:
        self._date = change_trend_date
        self._trend = is_up_trend

    def is_up_trend(self):
        return self._trend

    def get_date(self):
        return self._date

    @classmethod
    def check_initial_trend(cls, candles: pd.DataFrame, sma: Sma, sma_duration: int):
        if sma is None:
            return None

        default_price = (candles['High'].iloc[sma_duration - 1] +
                         candles['Low'].iloc[sma_duration - 1]) / 2
        change_trend_date = candles[-1:].index[0]
        if sma.get_sma()['Price'].iloc[sma_duration-1] < default_price:
            return cls(change_trend_date, True)
        else:
            return cls(change_trend_date, False)

    @classmethod
    def check_trend(cls, candles: pd.DataFrame, sma: Sma, current_trend: bool):
        change_trend_date = candles[-1:].index[0]
        if current_trend:
            if candles['High'].iloc[-2] < sma.get_sma()['Price'].iloc[-1]:
                return cls(change_trend_date, not current_trend)
        else:
            if candles['Low'].iloc[-2] > sma.get_sma()['Price'].iloc[-1]:
                return cls(change_trend_date, not current_trend)
        return cls(change_trend_date, current_trend)


class TrendHistory:
    def __init__(self, prevent_trend: Optional[Trend] = None, current_trend: Optional[Trend] = None) -> None:
        self._current_trend = current_trend
        self._prevent_trend = prevent_trend
        self._is_cahnged = False

    def is_changed(self):
        return self._is_cahnged

    def change_history(self, current_trend: Optional[Trend]):
        if self._current_trend is None:
            self._current_trend = current_trend
        if self._current_trend.is_up_trend() == current_trend.is_up_trend():
            self._is_cahnged = False
            return

        self._prevent_trend = self._current_trend
        self._current_trend = current_trend
        self._is_cahnged = True

    def get_histories(self) -> list[Trend]:
        return [self._current_trend, self._prevent_trend]
