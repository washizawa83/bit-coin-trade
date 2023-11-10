import threading
import time
import tkinter
from finance.finance import Candle, Ticker
from finance.local_app.gui import GuiApp
from finance.settings import Settings
from indicators.indicators import Sma
from indicators.trend import Trend, TrendHistory


class Trade:
    def collection_data(self):
        ticker = Ticker.create_ticker()
        candle = Candle(ticker)
        settings = Settings()
        trend = Trend
        trend_history = TrendHistory(None, None)
        is_collected_data = False

        while not is_collected_data:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candles = candle.create_candle(ticker)
            print(candles.iloc[-5:])
            if not candle.is_new_generated() or len(candles) < settings.sma_duration + 1:
                continue

            sma = Sma.create_sma(candles, settings.sma_duration)
            if len(candles) == settings.sma_duration + 1:
                trend = trend.check_initial_trend(
                    candles, sma, settings.sma_duration)
            else:
                trend = trend.check_trend(candles, sma, trend.is_up_trend())
            print(trend.is_up_trend())

            trend_history.change_history(trend)
            print(trend_history.get_histories())
            if None not in trend_history.get_histories():
                is_collected_data = True

        return candle, trend, trend_history

    def trade(self, candle: Candle, trend: Trend, trend_history: TrendHistory):
        settings = Settings()
        while True:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candles = candle.create_candle(ticker)
            if not candle.is_new_generated():
                continue

            sma = Sma.create_sma(candles, settings.sma_duration)
            trend = Trend.check_trend(
                candles, sma, trend.is_up_trend())
            trend_history.change_history(trend)

    def start(self):
        candle, trend, trend_history = self.collection_data()
        self.trade(candle, trend, trend_history)
