import yfinance as yf
import datetime
import yaml
import pandas as pd
from notify_run import Notify
from dateutil.relativedelta import relativedelta
from functools import lru_cache


class StockMovements:
    def __init__(self, path, period='weekly'):
        self.path = path
        self.holdings, self.tickers = self._read_config(path)
        self.period = period

    def __repr__(self):
        return f"StockMovements('{self.path}', {self.period}) #{self.tickers}"

    @staticmethod
    def _read_config(path):
        with open(path) as f:
            holdings = yaml.safe_load(f)

        return pd.DataFrame(holdings).T, ' '.join(holdings.keys())

    @lru_cache()
    def _fetch_price_data(self, end_date):
        start_date = end_date - relativedelta(months=1)

        df = (
            yf.download(
                tickers=self.tickers,
                start=start_date - relativedelta(days=7),
                end=end_date,
                interval='1d',
                progress=False,
            )
        )['Close']

        df_fill = df.reindex(
            pd.date_range(start=start_date, end=end_date, freq='D')
        ).fillna(method='ffill')

        change = (df_fill.iloc[-1] - df_fill.iloc[[0, -8]]).T
        change.columns = ['month_change', 'week_change']
        change['day_change'] = df_fill.iloc[-1] - df.iloc[-2]

        return change

    def get_returns(self, end_date=None):
        if end_date is None:
            end_date = datetime.date.today() - relativedelta(days=1)
        df = self._fetch_price_data(end_date).join(self.holdings)

        df['month_return'] = df.month_change * df.quantity
        df['week_return'] = df.week_change * df.quantity
        df['day_return'] = df.day_change * df.quantity

        return df

    def get_movement(self, period='week', end_date=None):
        if period not in ['day', 'week', 'month']:
            raise ValueError("supported periods are 'day', 'week', 'month'")

        return self.get_returns(end_date)[f'{period}_return'].sum()

    def notify_movement(self, period='week', end_date=None):
        movement = self.get_movement()
        Notify().send(
            f'Total movement in the last {period}:\n{"+" if movement >= 0 else "-"}${movement:.2f}'
        )
