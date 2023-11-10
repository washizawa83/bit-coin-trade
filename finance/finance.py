import datetime

import pandas as pd

from finance.api import ApiClient
from finance.settings import Settings
from utils.date_utils import ConvertDate


class Ticker:
    def __init__(self, ticker_datetime: str, mid_price: int, volume: int) -> None:
        self.datetime = ticker_datetime
        self.mid_price = mid_price
        self.volume = volume

    @classmethod
    def _get_ticker_mid_price(cls, ticker):
        return (ticker['best_ask'] + ticker['best_bid']) / 2

    @classmethod
    def _get_ticker_volume(cls, ticker):
        return ticker['volume']

    @classmethod
    def create_ticker(cls):
        api_client = ApiClient()
        ticker = api_client.fetch_ticker()
        settings = Settings()
        if ticker:
            ticker_timestamp = pd.Timestamp(
                ticker['timestamp']) + datetime.timedelta(hours=9)
            ticker_datetime = ConvertDate.convert_datetime_duration(
                ticker_timestamp, settings.duration)
            mid_price = cls._get_ticker_mid_price(ticker)
            volume = cls._get_ticker_volume(ticker)

            return Ticker(ticker_datetime, mid_price, volume)


class Candle:
    def __init__(self, ticker: Ticker):
        self._candles = pd.DataFrame(
            {
                'High': ticker.mid_price,
                'Open': ticker.mid_price,
                'Low': ticker.mid_price,
                'Close': ticker.mid_price,
                'Volume': ticker.volume,
            }, index=[ticker.datetime])
        self._candles.index.name = 'Date'
        self._is_generated = False

    def create_candle(self, ticker: Ticker) -> None:
        if ticker.datetime in self._candles.index:
            self._is_generated = False
            return self._update_candle(ticker)

        new_ticker = {
            ticker.datetime: [
                ticker.mid_price,
                ticker.mid_price,
                ticker.mid_price,
                ticker.mid_price,
                ticker.volume
            ]
        }
        self._candles = pd.concat(
            [self._candles,
             pd.DataFrame.from_dict(
                 new_ticker,
                 orient='index',
                 columns=['High', 'Open', 'Low', 'Close', 'Volume']
             )]
        )
        self._is_generated = True
        return self._candles

    def _update_candle(self, ticker: Ticker) -> None:
        if self._candles.loc[ticker.datetime]['High'] < ticker.mid_price:
            self._candles.loc[ticker.datetime, 'High'] = ticker.mid_price

        elif self._candles.loc[ticker.datetime]['Low'] > ticker.mid_price:
            self._candles.loc[ticker.datetime, 'Low'] = ticker.mid_price

        self._candles.loc[ticker.datetime, 'Close'] = ticker.mid_price
        self._candles.loc[ticker.datetime, 'Volume'] = ticker.volume

        return self._candles

    def is_new_generated(self):
        return self._is_generated

    def get_all_candles(self):
        return self._candles

    def get_candle_from_date_scope(self, start_date: str, end_date: str = None) -> pd.DataFrame:
        try:
            if end_date is None:
                return self.candles[start_date]
            return self.candles[start_date: end_date]
        except:
            print('Error: class Candles of get_candle_from_date_span function')

    def get_number_of_candle_from_date_scope(self, start_date: str, end_date: str) -> int:
        try:
            date_scope_candles = self._candles[start_date: end_date]
            return date_scope_candles.length
        except:
            print('Error class Candles of get_number_of_candle_from_date_scope function')
