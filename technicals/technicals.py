from finance.finance import Candle
from indicators.max_min_price import MaxMin


class TrendLine:
    scope = 50

    def __init__(self, registance_line, support_line) -> None:
        self._registance_line = registance_line
        self._support_line = support_line

    @classmethod
    def get_resistance_and_support_line(cls, candle: Candle):
        max_price = candle.get_all_candles.iloc[-cls.scope:]['High'].max()
        min_price = candle.get_all_candles.iloc[-cls.scope:]['Low'].min()
        return cls(max_price, min_price)

    def get_registance_line(self):
        return self._registance_line

    def get_support_line(self):
        return self._support_line


# TODO 三角保ち合い、ダブルトップ、ダブルボトムも判定に入れる
class TripleTop:
    def is_top__down_standard_value(candle: Candle, high_price: float, low_price: float):
        min_rate = 0.1
        trend_line = TrendLine.get_resistance_and_support_line(candle)
        max_difference = trend_line.get_registance_line() - trend_line.get_support_line()
        difference = high_price - low_price
        rate = difference / max_difference

        return min_rate < rate

    # 三尊
    @classmethod
    def check_triple_top(cls, candle: Candle, max_min: MaxMin):
        five_max_min = max_min.get_max_min().iloc[-5:]
        first_top, first_bottom, second_top, second_bottom, third_top = five_max_min[
            'Price'].values

        if not (first_bottom < first_top < second_top) and not (second_bottom < third_top < second_top):
            return False
        if not first_top < third_top:
            return False

        judgments = [
            cls.is_top__down_standard_value(
                candle, five_max_min.iloc[i]['Price'], five_max_min.iloc[i + 1]['Price'])
            if i < 4
            else cls.is_triple_top_above_standard_value(candle, five_max_min.iloc[i]['Price'], five_max_min.iloc[i - 1]['Price'])
            for i in range(0, 5, 2)
        ]

        if not all(judgments):
            return False

        return True

    # 逆三尊
    @classmethod
    def check_triple_bottom(cls, candle: Candle, max_min: MaxMin):
        five_max_min = max_min.get_max_min().iloc[-5:]
        first_bottom, first_top, second_bottom, second_top, third_bottom = five_max_min[
            'Price'].values

        if not (first_top > first_bottom > second_bottom) and not (second_top > third_bottom > second_bottom):
            return False
        if not first_bottom > third_bottom:
            return False

        judgments = [
            cls.is_top__down_standard_value(
                candle, five_max_min.iloc[i + 1]['Price'], five_max_min.iloc[i]['Price'])
            if i < 4
            else cls.is_triple_top_above_standard_value(candle, five_max_min.iloc[i - 1]['Price'], five_max_min.iloc[i]['Price'])
            for i in range(0, 5, 2)
        ]

        if not all(judgments):
            return False

        return True
