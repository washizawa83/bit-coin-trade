import tkinter as tk
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from finance.finance import Candle, Ticker, ApiClient


class GuiApp:
    def __init__(self, root) -> None:
        self.ticker = Ticker.create_ticker()
        self.candle = Candle(self.ticker)
        self.candles = self.candle.get_all_candles()
        self.api_client = ApiClient()
        self.style = self.get_style()
        self.sma_durations = [5]
        self.fig, self.axes = mpf.plot(
            self.candles, returnfig=True, type='candle', figsize=(11.5, 3.5), style=self.style)
        self.ax = self.axes[0]
        self.root = root

        self.root.title('Bit Coin Trade')
        self.root.geometry('1200x600+30+30')
        self.root.resizable(False, False)
        self.root.configure(bg='white')
        self.create_indicator(self.root)
        self.frame_graph, self.canvas = self.create_graph(self.root, self.fig)
        self.create_balance(self.root)
        self.create_history(self.root)
        self.create_order(self.root)
        self.create_signal(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def open_window(self, candles):
        self.ax.clear()
        self.canvas.get_tk_widget().destroy()
        # if candles['max_min'].count() > 0:
        #     addplot = mpf.make_addplot(candles['max_min'], ax=self.ax, type='scatter', markersize=150, marker='.',
        #                                color='#049DBF')
        #     mpf.plot(candles, ax=ax, type='candle', mav=self.sma_durations, style=style, addplot=addplot)
        #     mpf.plot(candles, ax=ax, type='candle', alines=[('2023-10-15 21:16:40', 4022887.5), ('2023-10-15 21:22:00', 4022887.5 + (20.9848 * 33))])
        # else:
        mpf.plot(candles, ax=self.ax, type='candle',
                 mav=self.sma_durations, style=self.style)
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor=tk.W)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.root.after(1000, self.open_window, self.canvas, self.ax)

    def quit_app(self, root):
        root.quit()
        root.destroy()

    def check_sma(self, duration):
        def inner():
            if duration in self.sma_durations:
                self.sma_durations.remove(duration)
            else:
                self.sma_durations.append(duration)
        return inner

    def create_indicator(self, root):
        frame_indicator = tk.Frame(root, bg='white', relief=tk.GROOVE, bd=1)
        frame_indicator.place(x=20, y=20, width=200, height=320)

        var = tk.BooleanVar()
        var.set(False)

        indicator_label = tk.Label(frame_indicator, text='Indicator', font=(
            'MS UI Gothic', 16), fg='#222', width=18)
        volume = tk.Checkbutton(frame_indicator, text='Volume', bg='white', font=(
            'MS UI Gothic', 14), fg='#222')
        sma = tk.Label(frame_indicator, text='SMA', bg='white',
                       font=('MS UI Gothic', 14), fg='#222')
        sma_10 = tk.Checkbutton(frame_indicator, text='10M', bg='white', font=('MS UI Gothic', 12),
                                fg='#222', command=self.check_sma(10), variable=var)
        sma_15 = tk.Checkbutton(frame_indicator, text='15M', bg='white', font=('MS UI Gothic', 12),
                                fg='#222', command=self.check_sma(15))
        sma_1 = tk.Checkbutton(frame_indicator, text='1H', bg='white', font=('MS UI Gothic', 12),
                               fg='#222', command=self.check_sma(60))
        bb = tk.Checkbutton(frame_indicator, text='Bollinger Bands', bg='white', font=(
            'MS UI Gothic', 14), fg='#222')
        ichimoku = tk.Checkbutton(frame_indicator, text='Ichimoku', bg='white', font=(
            'MS UI Gothic', 14), fg='#222')
        indicator_label.grid(row=0, column=0, columnspan=3)
        sma.grid(row=1, column=0, sticky=tk.W, columnspan=3, pady=5)
        sma_10.grid(row=2, column=0, pady=5)
        sma_15.grid(row=2, column=1, sticky=tk.W)
        sma_1.grid(row=2, column=2, sticky=tk.W)
        volume.grid(row=3, column=0, sticky=tk.W, columnspan=3, pady=5)
        bb.grid(row=4, column=0, sticky=tk.W, columnspan=3, pady=5)
        ichimoku.grid(row=5, column=0, sticky=tk.W, columnspan=3, pady=5)

    def create_graph(self, root, fig):
        frame_graph = tk.Frame(root, relief=tk.FLAT, bg='white')
        frame_graph.place(x=50, y=0, width=1500, height=350)
        frame_graph.lower()

        canvas = FigureCanvasTkAgg(fig, frame_graph)
        canvas.get_tk_widget().pack()

        return frame_graph, canvas

    def create_balance(self, root):
        mid_price = self.api_client.fetch_ticker()['best_bid']
        jpy, btc, total, delta = self.api_client.get_balance(mid_price)

        frame_balance = tk.Frame(root, bg='white', relief=tk.GROOVE, bd=1)
        frame_balance.place(x=20, y=360, width=200, height=220)

        balance_label = tk.Label(frame_balance, text='Balance', font=(
            'MS UI Gothic', 16), width=18, fg='#222')
        balance_label.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.S)

        jpy_label = tk.Label(frame_balance, text='日本円', font=(
            'MS UI Gothic', 12), bg='white', fg='#222')
        jpy_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        jpy_amount_label = tk.Label(frame_balance, text=str(
            jpy)+' 円', font=('MS UI Gothic', 12), bg='white', fg='#222')
        jpy_amount_label.grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)

        btc_label = tk.Label(frame_balance, text='Bitcoin', font=(
            'MS UI Gothic', 12), bg='white', fg='#222')
        btc_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        btc_amount_label = tk.Label(frame_balance, text=str(
            btc) + ' BTC', font=('MS UI Gothic', 12), bg='white', fg='#222')
        btc_amount_label.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

        delta_label = tk.Label(frame_balance, text='デルタ', font=(
            'MS UI Gothic', 12), bg='white', fg='#222')
        delta_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        delta_amount_label = tk.Label(frame_balance, text=str(
            delta) + ' 円', font=('MS UI Gothic', 12), bg='white', fg='#222')
        delta_amount_label.grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)

        total_label = tk.Label(frame_balance, text='純資産', font=(
            'MS UI Gothic', 12), bg='white', fg='#222')
        total_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        total_amount_label = tk.Label(frame_balance, text=str(
            total) + ' 円', font=('MS UI Gothic', 12), bg='white', fg='#222')
        total_amount_label.grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)

        pl_label = tk.Label(frame_balance, text='損益', font=(
            'MS UI Gothic', 12), bg='white', fg='#222')
        pl_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        pl_amount_label = tk.Label(frame_balance, text=str(
            0) + ' 円', font=('MS UI Gothic', 12), bg='white', fg='#222')
        pl_amount_label.grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)

    def create_history(self, root):
        menu = ['日付', '売・買', '取引数量', '価格', 'ステータス']
        histories = self.api_client.order_histories()

        frame_history = tk.Frame(root, bg='white', relief=tk.GROOVE, bd=1)
        frame_history.place(x=240, y=360, width=565, height=220)

        order_history_label = tk.Label(frame_history, text='取引履歴', font=(
            'MS UI Gothic', 14), width=56, fg='#222')
        order_history_label.grid(
            row=0, column=0, columnspan=5, sticky=tk.W + tk.S)
        for i, m in enumerate(menu):
            order_history_menu_label = tk.Label(
                frame_history, text=m, font=('MS UI Gothic', 12), width=11, fg='#222')
            order_history_menu_label.grid(
                row=1, column=i, sticky=tk.W + tk.S, ipadx=4, ipady=3)

        for i, his in enumerate(histories):
            if i <= 5:
                date_label = tk.Label(frame_history, text=his[0], font=(
                    'MS UI Gothic', 10), bg='white', width=12, fg='#222')
                date_label.grid(row=i+2, column=0,
                                sticky=tk.W + tk.S, ipadx=10, ipady=3)

                if his[1] == '売り':
                    side_label = tk.Label(frame_history, text=his[1], font=('MS UI Gothic', 10), bg='white', width=12,
                                          fg='#FF3333')
                    side_label.grid(row=i + 2, column=1,
                                    sticky=tk.W + tk.S, ipadx=10, ipady=3)
                else:
                    side_label = tk.Label(frame_history, text=his[1], font=('MS UI Gothic', 10), bg='white', width=12,
                                          fg='#33CC66')
                    side_label.grid(row=i + 2, column=1,
                                    sticky=tk.W + tk.S, ipadx=10, ipady=3)

                size_label = tk.Label(frame_history, text=his[2], font=(
                    'MS UI Gothic', 10), bg='white', width=12, fg='#222')
                size_label.grid(row=i + 2, column=2,
                                sticky=tk.W + tk.S, ipadx=10, ipady=3)

                price_label = tk.Label(frame_history, text=his[3], font=(
                    'MS UI Gothic', 10), bg='white', width=12, fg='#222')
                price_label.grid(row=i + 2, column=3,
                                 sticky=tk.W + tk.S, ipadx=10, ipady=3)

                status_label = tk.Label(frame_history, text=his[4], font=(
                    'MS UI Gothic', 10), bg='white', width=12, fg='#222')
                status_label.grid(row=i + 2, column=4,
                                  sticky=tk.W + tk.S, ipadx=10, ipady=3)

    def create_order(self, root):
        frame_order = tk.Frame(root, bg='white')
        frame_order.place(x=825, y=360, width=330, height=80)

        sell_button = tk.Button(frame_order, text='SELL', font=('Clarimo UD PE', 23), bg='#FF6666', fg='#FFF',
                                width=6, height=2, relief=tk.GROOVE, command=self.api_client.sell_order)
        sell_button.grid(row=0, column=0, ipadx=10, padx=30)
        buy_button = tk.Button(frame_order, text='BUY', font=('Clarimo UD PE', 23), bg='#90EE90', fg='#FFF',
                               width=6, height=2, relief=tk.GROOVE, command=self.api_client.buy_order)
        buy_button.grid(row=0, column=1, ipadx=10, sticky=tk.E)

    def create_signal(self, root):
        frame_signal = tk.Frame(root, bg='white', relief=tk.GROOVE, bd=1)
        frame_signal.place(x=825, y=460, width=350, height=120)

        balance_label = tk.Label(frame_signal, text='Signal', font=(
            'MS UI Gothic', 16), width=32, fg='#222')
        balance_label.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.S)

    def get_style(self):
        return {'base_mpl_style': 'fast',
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
