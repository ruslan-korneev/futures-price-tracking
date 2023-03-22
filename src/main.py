import asyncio

from src import settings
from src.tracking import Tracker

logger = settings.logging.getLogger(__name__)


def main():
    logger.debug("initialize tracker...")
    tracker = Tracker()
    logger.debug(
        f"start tracking {tracker.tracked_symbol} "
        f"with influence by {tracker.influencing_symbol}"
    )
    asyncio.run(tracker.start())


if __name__ == "__main__":
    main()
