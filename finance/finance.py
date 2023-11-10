import datetime

import pandas as pd

from finance.api import ApiClient
from finance.settings import Settings
from utils.date_utils import ConvertDate


class Ticker:
    def __init__(self, ticker_datetime: str, mid_price: float, volume: int) -> None:
        self._datetime = ticker_datetime
        self._mid_price = mid_price
        self._volume = volume

    def get_datetime(self) -> str:
        return self._datetime

    def get_mid_price(self) -> float:
        return self._mid_price

    def get_volume(self) -> float:
        return self._volume

    @classmethod
    def _get_ticker_mid_price(cls, ticker) -> float:
        return (ticker['best_ask'] + ticker['best_bid']) / 2

    @classmethod
    def _get_ticker_volume(cls, ticker) -> float:
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

            return cls(ticker_datetime, mid_price, volume)


class Candle:
    def __init__(self, ticker: Ticker):
        self._candles = pd.DataFrame(
            {
                'High': ticker.get_mid_price(),
                'Open': ticker.get_mid_price(),
                'Low': ticker.get_mid_price(),
                'Close': ticker.get_mid_price(),
                'Volume': ticker.get_volume(),
            }, index=[ticker.get_datetime()])
        self._candles.index.name = 'Date'
        self._is_generated = False

    def create_candle(self, ticker: Ticker) -> pd.DataFrame:
        if ticker.get_datetime() in self._candles.index:
            self._is_generated = False
            return self._update_candle(ticker)

        new_ticker = {
            ticker.get_datetime(): [
                ticker.get_mid_price(),
                ticker.get_mid_price(),
                ticker.get_mid_price(),
                ticker.get_mid_price(),
                ticker.get_volume()
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

    def _update_candle(self, ticker: Ticker) -> pd.DataFrame:
        if self._candles.loc[ticker.get_datetime()]['High'] < ticker.get_mid_price():
            self._candles.loc[ticker.get_datetime(
            ), 'High'] = ticker.get_mid_price()

        elif self._candles.loc[ticker.get_datetime()]['Low'] > ticker.get_mid_price():
            self._candles.loc[ticker.get_datetime(
            ), 'Low'] = ticker.get_mid_price()

        self._candles.loc[ticker.get_datetime(
        ), 'Close'] = ticker.get_mid_price()
        self._candles.loc[ticker.get_datetime(
        ), 'Volume'] = ticker.get_volume()

        return self._candles

    def is_new_generated(self) -> bool:
        return self._is_generated

    def get_all_candles(self) -> pd.DataFrame:
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
