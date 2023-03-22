import asyncio
from binance.client import Client

from src import settings
from src.services import async_get, get_correlation

logger = settings.logging.getLogger(__name__)


class Symbol:
    def __init__(self, title: str) -> None:
        self.title = title

    async def get_price(self, base_api: str = settings.BASE_API):
        """Get price for currency"""
        data = await async_get(f"{base_api}/ticker/price", symbol=self.title)
        return float(data["price"])


class Tracker:
    def __init__(
        self,
        tracked_symbol: str = settings.DEFAULT_TRACKED_SYMBOL,
        influencing_symbol: str = settings.DEFAULT_INFLUENCING_SYMBOL,
        limit: int = settings.DEFAULT_LIMIT,
        tracking_interval: str = settings.TRACKING_INTERVAL,
        api_key: str | None = settings.API_KEY,
        api_secret: str | None = settings.API_SECRET,
        base_api: str = settings.BASE_API,
    ) -> None:
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.tracked_symbol = Symbol(tracked_symbol)
        self.influencing_symbol = Symbol(influencing_symbol)
        self.limit = limit
        self.tracking_interval = tracking_interval
        self.base_api = base_api

    async def start(self):
        """Live Tracking price changes"""
        exclude_influence = 0

        while True:
            tracked_price = await self.calculate_tracked_symbol_price(exclude_influence)
            logger.debug(f"Tracked price: {tracked_price}")
            logger.debug(
                f"sleep ... for {settings.TRACKING_INTERVAL_IN_SECONDS} seconds"
            )
            await asyncio.sleep(settings.TRACKING_INTERVAL_IN_SECONDS)
            tracked_price_last_hour = await self.calculate_tracked_symbol_price(
                exclude_influence
            )
            logger.debug(f"Tracked price after sleep: {tracked_price_last_hour}")

            tracked_price_change = (tracked_price_last_hour / tracked_price) - 1
            logger.debug(f"[Debug information] Changes: {tracked_price_change * 100:.2f}%")
            if abs(tracked_price_change) >= 0.001:
                logger.info(f"Changes: {tracked_price_change * 100:.2f}%")

            exclude_influence = tracked_price_change

    async def calculate_tracked_symbol_price(self, exclude_influence: float) -> float:
        """
        Calculate price for Tracked Symbol
        Excluding Influencing Symbol's movements
        """
        tracked_price = await self.tracked_symbol.get_price()
        inf_price = await self.influencing_symbol.get_price()
        influence = await self.get_influence()
        tracked_price -= inf_price * influence * exclude_influence
        return tracked_price

    async def get_influence(self):
        """Get coef of influence"""
        tracked_params = {
            "symbol": self.tracked_symbol.title,
            "interval": self.tracking_interval,
            "limit": self.limit,
        }
        tracked_data = await async_get(f"{self.base_api}/klines", **tracked_params)

        inf_params = {
            "symbol": self.influencing_symbol.title,
            "interval": self.tracking_interval,
            "limit": self.limit,
        }
        inf_data = await async_get(f"{self.base_api}/klines", **inf_params)
        return get_correlation(tracked_data, inf_data)
