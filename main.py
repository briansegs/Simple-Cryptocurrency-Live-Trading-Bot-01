import time
import pandas as pd
import sqlalchemy
from kucoin_futures.client import WsToken
from kucoin_futures.ws_client import KucoinFuturesWsClient
import config as c
import asyncio

def createframe(msg):
    df = pd.DataFrame([msg['data']])
    df = df.iloc[:,[0, 5, 3]]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ns')
    return df

async def main():
    engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
    async def deal_msg(msg):
        frame = createframe(msg)
        time.sleep(2)
        frame.to_sql('BTCUSDT', engine, if_exists='append', index=False)
        print(frame)


    client = WsToken(
        key=c.kc_futures['API_KEY'],
        secret=c.kc_futures['API_SECRET'],
        passphrase=c.kc_futures['API_PASSPHRASE'],
        )

    print('1')
    ws_client = await KucoinFuturesWsClient.create(loop, client, deal_msg, private=False)
    print('2')
    await ws_client.subscribe("/contractMarket/tickerV2:XBTUSDM")
    print('3')
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())