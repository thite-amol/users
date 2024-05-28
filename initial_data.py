"""Module."""

import asyncio
import logging

from src.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    """_summary_."""
    await init_db()


async def main() -> None:
    """_summary_."""
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
