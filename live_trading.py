import sqlalchemy
import pandas as pd
from kucoin_futures.client import WsToken
from kucoin_futures.ws_client import KucoinFuturesWsClient
import config as c

engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')

df = pd.read_sql('BTCUSDT', engine)

# Trend following
# if price rising by x % -> Buy
# exut when profit is above 0.15% or loss is crossing -0.15%