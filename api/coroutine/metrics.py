"""Module for getting data from metrics generator asynchronously."""
import asyncio

import aiohttp

from metrics_generator.settings import (
    METRICS_GEN_SERVICE_PORT,
    METRICS_GEN_SERVICE_HOST,
)


async def get(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_resource_task(portion_amount) -> list[str]:
    url = f"http://{METRICS_GEN_SERVICE_HOST}:{METRICS_GEN_SERVICE_PORT}/generate_metrics/"

    async with aiohttp.ClientSession() as session:
        tasks = [get(session, url=url + str(num)) for num in range(portion_amount)]
        raw_data = await asyncio.gather(*tasks)

    return raw_data
