import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mplfinance as mpf

from finance.finance import Candle
from finance.settings import Settings


class ChartPlot:
    trade = None
    candle = None
    settings = Settings()
    ax = None

    style = {'base_mpl_style': 'fast',
             'marketcolors': {'candle': {'up': '#33CC66', 'down': '#FF3333'},
                              'edge': {'up': '#33CC66', 'down': '#FF3333'},
                              'wick': {'up': '#FFF', 'down': '#FFF'},
                              'ohlc': {'up': '#33CC66', 'down': '#FF3333'},
                              'volume': {'up': '#33CC66', 'down': '#FF3333'},
                              'vcedge': {'up': '#33CC66', 'down': '#FF3333'},
                              'vcdopcod': False,
                              'alpha': 0.9},
             'mavcolors': None,
             'facecolor': '#333',
             'figcolor': '#333',
             'gridcolor': '#666',
             'gridstyle': None,
             'y_on_right': True,
             'rc': {'axes.edgecolor': '#f8f8ff',
                    'axes.grid':  True,
                    'axes.grid.axis': 'y',
                    'axes.labelcolor': 'white',
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'grid.color': '#000000',
                    'grid.linestyle': '-'
                    },
             'base_mpf_style': 'None'
             }

    @classmethod
    def update_plot(cls, frame):
        cls.ax.clear()
        if cls.trade.max_min is not None:
            candles = cls.candle.get_all_candles()
            max_min = cls.trade.max_min.get_max_min()
            join = candles.join(max_min)
            add_plot = mpf.make_addplot(
                join['Price'], ax=cls.ax, type='scatter', markersize=150, marker='.', color='#049DBF')
            mpf.plot(cls.candle.get_all_candles(), type='candle',
                     mav=cls.settings.sma_duration, ax=cls.ax, style=cls.style, addplot=add_plot)
        else:
            mpf.plot(cls.candle.get_all_candles(),
                     type='candle', mav=cls.settings.sma_duration, ax=cls.ax, style=cls.style)

    @classmethod
    def plot(cls, candle: Candle):
        cls.candle = candle
        fig, axes = mpf.plot(candle.get_all_candles(), returnfig=True, type='candle',
                             figsize=(11.5, 3.5), style=cls.style)
        cls.ax = axes[0]
        ani = FuncAnimation(fig, cls.update_plot,
                            interval=1000, cache_frame_data=False)
        plt.show()

    @classmethod
    def plot2(cls, trade):
        cls.trade = trade
        cls.candle = trade.candle

        fig, axes = mpf.plot(cls.candle.get_all_candles(), returnfig=True, type='candle',
                             figsize=(11.5, 3.5), style=cls.style)
        cls.ax = axes[0]
        ani = FuncAnimation(fig, cls.update_plot,
                            interval=1000, cache_frame_data=False)
        plt.show()
