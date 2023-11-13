import threading
import time
from finance.local_app.gui import ChartPlot
from trade import Trade


if __name__ == '__main__':
    trade = Trade()
    # trade.start()
    plot_thread = threading.Thread(target=trade.start)
    plot_thread.start()

    while trade.candle is None:
        time.sleep(1)

    ChartPlot.plot(trade)
