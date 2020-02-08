import os
import datetime
import yaml
from dateutil.relativedelta import relativedelta
from functools import lru_cache
import pandas as pd
import yfinance as yf
import pystache
from notify_run import Notify


class StockMovements:
    def __init__(self, path: str):
        self.path = path
        self.config = self._read_config(path)

        self.holdings = pd.DataFrame(self.config['stocks']).T
        self.tickers = ' '.join(self.config['stocks'])

    def __repr__(self):
        return f"StockMovements('{self.path}', {self.config['period']}) #{self.tickers}"

    @staticmethod
    def _read_config(path: str) -> dict:
        with open(os.path.expanduser(path)) as f:
            return yaml.safe_load(f)

    @lru_cache()
    def _fetch_price_data(self):
        end_date = datetime.date.today()
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

    def get_returns(self):
        df = self._fetch_price_data().join(self.holdings)

        df['month_return'] = df.month_change * df.quantity
        df['week_return'] = df.week_change * df.quantity
        df['day_return'] = df.day_change * df.quantity

        return df

    def get_gain(self):
        if self.config['period'] not in ['day', 'week', 'month']:
            raise ValueError("supported periods are 'day', 'week', 'month'")

        return self.get_returns()[f'{self.config["period"]}_return'].sum()

    def get_gain_formatted(self):
        gain = self.get_gain()
        return f'{"+" if gain >= 0 else "-"}${gain:.2f}'

    def _prepare_message(self, other):
        config = self.config.copy()

        if 'message' not in config:
            config['message'] = '{{gain}}'

        return config.pop('message'), {**config, **other}

    def notify_gain(self):
        Notify().send(
            pystache.render(*self._prepare_message({'gain': self.get_gain_formatted()}))
        )
