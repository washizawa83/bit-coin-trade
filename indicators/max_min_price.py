import pandas as pd

from indicators.trend import TrendHistory


class MaxMin:
    def __init__(self, max_min_date, max_min_price) -> None:
        self._max_min = pd.DataFrame(
            {
                'Price': max_min_price,
            }, index=[max_min_date])
        self._candles.index.name = 'Date'

    @classmethod
    def extraction_max_min_from_trend_histories(cls, candles: pd.DataFrame, trend_history: TrendHistory):
        histories = trend_history.get_history()
        max_min_date = ''
        max_min_price = 0

        if histories[0].is_up_trend():
            max_min_date = candles[histories[1].get_date(
            ): histories[0].get_date()]['Low'].idxmin()
            max_min_price = candles.loc[max_min_date]['Low']
        else:
            max_price_date = candles[histories[1].get_date(
            ): histories[0].get_date()]['High'].idxmax()
            max_min_price = candles.loc[max_price_date]['High']

        return max_min_date, max_min_price

    @classmethod
    def create_max_min(cls, candles: pd.DataFrame, trend_history: TrendHistory):
        max_min_date, max_min_price = cls.extraction_max_min_from_trend_histories(
            candles, trend_history)
        return cls(max_min_date, max_min_price)

    def update_max_min(self, candles: pd.DataFrame, trend_history: TrendHistory):
        max_min_date, max_min_price = self.extraction_max_min_from_trend_histories(
            candles, trend_history)

        new_max_min = {
            max_min_date: [max_min_price]
        }
        pd.concat([self._max_min,
                   pd.DataFrame.from_dict(
                       new_max_min,
                       orient='index',
                       columns=['Price']
                   )]
                  )

    def get_max_min(self):
        return self._max_min
