import datetime
import pandas as pd

import pybitflyer

from utils.date_utils import ConvertDate
from .settings import Settings


class ApiClient:
    def __init__(self) -> None:
        self._settings = Settings()
        self._api = pybitflyer.API(
            api_key=self._settings.api_key,
            api_secret=self._settings.api_secret
        )

    def fetch_ticker(self):
        try:
            return self._api.ticker()
        except:
            print('Error fetch_ticker function is class ApiClient')

    def get_balance(self, mid_price: float):
        balance = self._api.getbalance()
        jpy = balance[0]['amount']
        btc = balance[1]['amount']
        delta = int(mid_price * btc)
        total = jpy + delta
        return jpy, btc, total, delta

    def buy_order(self):
        order = self._api.sendchildorder(
            product_code='BTC_JPY',
            child_order_type='MARKET',
            side='BUY',
            size=0.001,
            minute_to_expire=10000,
            time_in_force='GTC'
        )
        return order

    def sell_order(self):
        order = self._api.sendchildorder(
            product_code='BTC_JPY',
            child_order_type='MARKET',
            side='SELL',
            size=0.001,
            minute_to_expire=10000,
            time_in_force='GTC'
        )
        return order

    def order_histories(self) -> list:
        side_status = {'BUY': '買い', 'SELL': '売り'}
        order_status = {'COMPLETED': '取引済み', 'CANCELED': 'キャンセル',
                        'EXPIRED': '有効期限切れ', 'REJECTED': '取引失敗'}
        convert_date = ConvertDate()
        histories_data = self._api.getchildorders()
        histories = []
        for history in histories_data:
            date = pd.Timestamp(
                history['child_order_date']) + datetime.timedelta(hours=9)
            date = convert_date.convert_display_date(date)
            side = side_status[history['side']]
            status = order_status[history['child_order_state']]
            histories.append([date, side, history['size'],
                             history['average_price'], status])
        return histories
