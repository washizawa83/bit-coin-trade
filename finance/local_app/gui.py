import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mplfinance as mpf

from finance.finance import Candle
from finance.settings import Settings


class ChartPlot:
    candle = None
    settings = Settings()
    ax = None

    style = {'base_mpl_style': 'fast',
             'marketcolors': {'candle': {'up': '#33CC66', 'down': '#FF3333'},
                              'edge': {'up': '#33CC66', 'down': '#FF3333'},
                              'wick': {'up': '#6633FF', 'down': '#6633FF'},
                              'ohlc': {'up': '#33CC66', 'down': '#FF3333'},
                              'volume': {'up': '#33CC66', 'down': '#FF3333'},
                              'vcedge': {'up': '#33CC66', 'down': '#FF3333'},
                              'vcdopcod': False,
                              'alpha': 0.9},
             'mavcolors': None,
             'facecolor': '#FFFFFF',
             'gridcolor': '#FF69B4',
             'gridstyle': None,
             'y_on_right': True,
             'rc': {'axes.edgecolor': '#f8f8ff',
                    'axes.grid':  True,
                    'axes.grid.axis': 'y',
                    'grid.color': '#000000',
                    'grid.linestyle': '--'
                    },
             'base_mpf_style': 'None'
             }

    @classmethod
    def update_plot(cls, frame):
        cls.ax.clear()
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
