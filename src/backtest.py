from datetime import date
import pandas as pd
import backtrader as bt


def loadBinanceData(filename: str) -> pd.DataFrame:
    raw = pd.read_csv(
        filename,
        header=None,
        usecols=range(0, 6),
        names=["datetime", "high", "low", "open", "close", "volume"]
    )
    raw["datetime"] = raw["datetime"].apply(lambda x: pd.to_datetime(x/1000, unit='s'))
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


if __name__ == '__main__':
    symbol = 'BTCUSDT'
    interval = '1d'
    pfast = 20
    pslow = 50
    cash = 10000

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    #cerebro.addsizer(bt.sizers.AllInSizer)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.PandasData(
        dataname=loadBinanceData(f"data/{symbol}-{interval}.dat"),
        fromdate=date(2015,1,1),
        todate=date(2020,12,31),
    )
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross, pfast=pfast, pslow=pslow)
    start_portfolio_value = cerebro.broker.getvalue()
    cerebro.run()
    
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    
    print(f'{symbol} PnL: {pnl:.2f}')
    cerebro.plot()
