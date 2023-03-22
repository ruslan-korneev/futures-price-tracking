import os
import logging


# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Consts
BASE_API = "https://api.binance.com/api/v3"
DEFAULT_TRACKED_SYMBOL = "ETHUSDT"
DEFAULT_INFLUENCING_SYMBOL = "BTCUSDT"
DEFAULT_LIMIT = 500
TRACKING_INTERVAL = "1h"
TRACKING_INTERVAL_IN_SECONDS = 60 * 60
CHANGES_PERCENT = 1 / 100

API_KEY = os.environ.get("API_KEY", None)
API_SECRET = os.environ.get("API_SECRET", None)
