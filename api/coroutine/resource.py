"""Module for getting data from metrics generator asynchronously."""
import asyncio

import aiohttp

from api.cfg import (
    METRICS_GEN_SERVICE_PORT,
    METRICS_GEN_SERVICE_HOST,
    METRICS_GEN_SERVICE_ENDPOINT,
)


async def get(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_resource_task(portion_amount: int) -> list[str]:
    url = f"http://{METRICS_GEN_SERVICE_HOST}:{METRICS_GEN_SERVICE_PORT}/{METRICS_GEN_SERVICE_ENDPOINT}"

    async with aiohttp.ClientSession() as session:
        tasks = [get(session, url=f"{url}/{num}") for num in range(portion_amount)]
        raw_data = await asyncio.gather(*tasks)

    return raw_data
