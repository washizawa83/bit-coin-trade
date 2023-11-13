from indicators.max_min_price import MaxMin


class TripleTop:
    @classmethod
    def check_triple_top(cls, max_min: MaxMin):
        five_max_min = max_min.get_max_min().iloc[-5:]
        first_top, first_bottom, second_top, second_bottom, third_top = five_max_min[
            'Price'].values

        if not (first_bottom < first_top < second_top) and not (second_bottom < third_top < second_top):
            return False
        if not first_top < third_top:
            return False

        return True
