import time
import tkinter as tk
from finance.finance import Candle, Ticker
from finance.local_app.gui import GuiApp

from finance.settings import Settings
from indicators.indicators import Sma
from indicators.trend import Trend, TrendHistory
from trade import Trade


if __name__ == '__main__':
    trade = Trade()
    trade.start()
