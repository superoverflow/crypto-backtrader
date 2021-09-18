## Goal 
- Would like to test which of the below strategy is best
- HODL vs SMA
- SMA Cross Currency (TBC)

## Parameters
- Lot size: 1k USD
- Time frame: 1year
- Kline: 1h 4h 1d
- SSMA: 10 20
- LSMA: 50 100 200

## How to download data?
```
cd scripts
./download.sh
```

## Pre-requisite
```
sudo apt-get install python3-tk
python -m venv venv
```


## How to download histroical trade data?
```
cd scripts
./download.sh
```

## How to run 
```
source venv/bin/activate
pip install -r requirement.txt
python backtest.py
```



