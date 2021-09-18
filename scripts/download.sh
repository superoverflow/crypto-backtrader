#!/bin/bash

# This is a simple script to download klines by given parameters.

symbols=("BTCUSDT" "ETHUSDT" "ADAUSDT" "XLMUSDT" "LTCUSDT" "EOSUSDT") # add symbols here to download
intervals=("15m" "1h" "4h" "12h" "1d")
years=("2017" "2018" "2019" "2020" "2021")
months=(01 02 03 04 05 06 07 08 09 10 11 12)

baseurl="https://data.binance.vision/data/spot/monthly/klines"

for symbol in ${symbols[@]}; do
  for interval in ${intervals[@]}; do
    for year in ${years[@]}; do
      for month in ${months[@]}; do
        url="${baseurl}/${symbol}/${interval}/${symbol}-${interval}-${year}-${month}.zip"
        response=$(wget --server-response -q ${url} 2>&1 | awk 'NR==1{print $2}')
        if [ ${response} == '404' ]; then
          echo "File not exist: ${url}" 
        else
          echo "downloaded: ${url}"
        fi
      done
    done
  ls -l *.zip | awk '{print $9}'  | xargs -I {} unzip {}
  rm *.zip
  ls -l *.csv | awk '{print $9}'  | xargs cat > ../data/${symbol}-${interval}.dat
  rm *.csv
  done
done

