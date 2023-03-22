# Futures price tracking

## Requirements
- [python >= 3.10](https://www.python.org/)
- [poetry](https://python-poetry.org/)

## Installation and Run
```zsh
git clone https://github.com/shaggy-axel/futures-price-tracking.git
cd futures-price-tracking
poetry install
track
```

## Description
Python script that tracks the price of `ETHUSDT` futures in real-time and determines its own movement of `ETH` price based on correlation method.
When the price changes by `1%` in the last `60 minutes`, the program outputs a message to the console. The program should continue to work, constantly reading the current price.

## [Default Settings](src/settings.py):
```
TRACKED Futures - ETHUSDT
Influencing Futures - BTCUSDT
Tracking interval - 1 hour
Changes in percent - 1 %
```
