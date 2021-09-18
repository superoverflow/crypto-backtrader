import pandas as pd
import backtrader as bt

def loadBinanceData():
    raw = pd.read_csv(
        "data/BTCUSDT-1d.dat",
        header=None,
        usecols=range(0, 6),
        names=["datetime", "high", "low", "open", "close", "volume"]
    )
    raw["datetime"] = raw["datetime"].apply(lambda x: pd.to_datetime(x/1000))
    raw = raw.set_index('datetime')
    return raw

class SmaCross(bt.Strategy):
    params = dict(
        pfast=20,
        pslow=50,
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()

        elif self.crossover < 0:
            self.close()


cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname=loadBinanceData())

cerebro.adddata(data)
cerebro.addstrategy(SmaCross)

start_portfolio_value = cerebro.broker.getvalue()
cerebro.run()
end_portfolio_value = cerebro.broker.getvalue()
pnl = end_portfolio_value - start_portfolio_value
print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
print(f'Final Portfolio Value: {end_portfolio_value:2f}')
print(f'PnL: {pnl:.2f}')
cerebro.plot()