import time
import sqlalchemy
import pandas as pd
from kucoin_futures.client import Trade
import config as c

engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')

df = pd.read_sql('BTCUSDT', engine)

# Trend following
# if price rising by x % -> Buy
# exut when profit is above 0.15% or loss is crossing -0.15%

def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql('BTCUSDT', engine)
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1
        if not open_position:
            if cumret[cumret.last_valid_index()] > entry:
                # order = Trade.create_market_order(symbol='XBTUSDM', side='Buy', lever=0)
                print(f'Buy: {qty} at {df.iloc[-1].Price} ')
                open_position = True
                break
        if open_position:
            while True:
                df = pd.read_sql('BTCUSDT', engine)
                sincebuy = df.loc[df.Time > pd.to_datetime(time.time(), unit='ms')]# order['transactTime']
                if len(sincebuy) > 1:
                    sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod() - 1
                    last_entry = sincebuyret[sincebuyret.last_valid_index()]
                    if last_entry > 0.0015 or last_entry < -0.0015:
                        # order = Trade.create_market_order(symbol='XBTUSDM', side='Sell', lever=0)
                        print(f'Huh!?')
                        break

strategy(0.001, 60, 0.001)