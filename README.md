# Futures price tracking

## Installation and Run
```zsh
git clone https://github.com/shaggy-axel/futures-price-tracking.git
poetry install
track
```

## Description
This is script which tracks the futures price, trying to determine the movement of that price based on correlation method. 
Determination of the price movement should not be influens by {INFLUENCING FUTURES} set up this futures in 

Python script that tracks the price of ETHUSDT futures in real-time and determines its own movement of ETH price based on correlation method.
When the price changes by 1% in the last 60 minutes, the program outputs a message to the console. The program should continue to work, constantly reading the current price.

## [Default Settings](src/settings.py):
```
TRACKED Futures - ETHUSDT
Influencing Futures - BTCUSDT
Tracking interval - 1 hour
Changes in percent - 1 %
```
