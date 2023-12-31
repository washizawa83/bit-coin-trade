import pandas as pd

from indicators.trend import TrendHistory


class MaxMin:
    def __init__(self, max_min_date, max_min_price) -> None:
        self._max_min = pd.DataFrame(
            {
                'Price': max_min_price,
            }, index=[max_min_date])
        self._max_min.index.name = 'Date'

    @classmethod
    def _extraction_max_min_from_trend_histories(cls, candles: pd.DataFrame, trend_history: TrendHistory):
        histories = trend_history.get_histories()
        start_candle_index = candles.index.get_loc(histories[1].get_date()) - 1
        start_candle_index_name = candles.iloc[start_candle_index].name

        if histories[0].is_up_trend():
            min_price_date = candles[start_candle_index_name: histories[0].get_date(
            )]['Low'].idxmin()
            min_price = candles.loc[min_price_date]['Low']
            return min_price_date, min_price
        else:
            max_price_date = candles[start_candle_index_name: histories[0].get_date(
            )]['High'].idxmax()
            max_price = candles.loc[max_price_date]['High']
            return max_price_date, max_price

    @classmethod
    def create_max_min(cls, candles: pd.DataFrame, trend_history: TrendHistory):
        max_min_date, max_min_price = cls._extraction_max_min_from_trend_histories(
            candles, trend_history)
        return cls(max_min_date, max_min_price)

    def update_max_min(self, candles: pd.DataFrame, trend_history: TrendHistory):
        max_min_date, max_min_price = self._extraction_max_min_from_trend_histories(
            candles, trend_history)

        new_max_min = {
            max_min_date: [max_min_price]
        }
        self._max_min = pd.concat([self._max_min,
                                   pd.DataFrame.from_dict(
                                       new_max_min,
                                       orient='index',
                                       columns=['Price']
                                   )]
                                  )

    def get_max_min(self):
        return self._max_min
