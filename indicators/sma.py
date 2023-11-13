import pandas as pd


class Sma:
    def __init__(self, sma: pd.DataFrame) -> None:
        self._sma = sma

    @classmethod
    def create_sma(cls, candles: pd.DataFrame, sma_duration: int):
        if len(candles) < sma_duration + 1:
            return None

        # TODO アベレージを算出する範囲を絞る(candles['Close'][:-1])
        sma = candles['Close'][:-
                               1].rolling(sma_duration).mean().to_frame('Price')
        sma.index.name = 'Date'
        return cls(sma)

    def get_sma(self):
        return self._sma
