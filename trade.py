import threading
import time

from finance.finance import Candle, Ticker
from finance.local_app.gui import ChartPlot
from finance.settings import Settings
from indicators.indicators import Sma
from indicators.max_min_price import MaxMin
from indicators.trend import Trend, TrendHistory


class Trade:
    ax = None
    candle = None
    max_min = None

    def collection_data(self):
        ticker = Ticker.create_ticker()
        self.candle = Candle(ticker)
        settings = Settings()
        trend = Trend
        trend_history = TrendHistory(None, None)
        is_collected_data = False

        while not is_collected_data:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candles = self.candle.create_candle(ticker)

            if not self.candle.is_new_generated() or len(candles) < settings.sma_duration + 1:
                continue

            sma = Sma.create_sma(candles, settings.sma_duration)
            if len(candles) == settings.sma_duration + 1:
                trend = trend.check_initial_trend(
                    candles, sma, settings.sma_duration)
            else:
                trend = trend.check_trend(
                    candles, sma, trend.is_up_trend())
            print(trend.is_up_trend())
            trend_history.change_history(trend)
            if None not in trend_history.get_histories():
                is_collected_data = True
                max_min = MaxMin.create_max_min(candles, trend_history)
                print(max_min.get_max_min())

        return trend, trend_history

    def trade(self, trend: Trend, trend_history: TrendHistory):
        settings = Settings()
        while True:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candles = self.candle.create_candle(ticker)

            if not self.candle.is_new_generated():
                continue

            sma = Sma.create_sma(candles, settings.sma_duration)
            trend = Trend.check_trend(
                candles, sma, trend.is_up_trend())
            trend_history.change_history(trend)

    def start(self):
        trend, trend_history = self.collection_data()
        self.trade(trend, trend_history)

    def start_gui(self):
        tread_thread = threading.Thread(target=self.start)
        tread_thread.start()

        # キャンドルが作成されるまで待機
        while self.candle is None:
            time.sleep(1)

        ChartPlot.plot(self.candle)
