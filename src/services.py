import aiohttp
import pandas as pd

from src.settings import logging

logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = (
    "Open time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close time",
    "Quote asset volume",
    "Number of trades",
    "Taker buy base asset volume",
    "Taker buy quote asset volume",
    "Ignore",
)


def get_correlation(tracked_data, inf_data) -> float:
    """
    get correlation based on tracked currency data
    and influencing currency data
    """
    logger.debug(f"getting correlation ...")
    inf_df = pd.DataFrame(inf_data, columns=list(REQUIRED_COLUMNS))
    inf_df["Open time"] = pd.to_datetime(inf_df["Open time"], unit="ms")
    inf_df["Close"] = inf_df["Close"].astype(float)

    tracked_df = pd.DataFrame(tracked_data, columns=list(REQUIRED_COLUMNS))
    tracked_df["Open time"] = pd.to_datetime(tracked_df["Open time"], unit="ms")
    tracked_df["Close"] = tracked_df["Close"].astype(float)

    df = pd.merge(
        inf_df[["Open time", "Close"]],
        tracked_df[["Open time", "Close"]],
        on="Open time",
    )

    return df["Close_x"].corr(df["Close_y"]) * 3


async def async_get(url: str, **params) -> dict:
    """Sends async get-request and returns data from response"""
    logger.debug(f"send get request to {url} with {params=}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
    return data
