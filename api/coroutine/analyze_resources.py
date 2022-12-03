"""Module for getting data asynchronously."""
import asyncio

import aiohttp

from metrics_generator.settings import (
    METRICS_GEN_SERVICE_PORT,
    METRICS_GEN_SERVICE_HOST,
    METRICS_GEN_ENDPOINT,
)


async def get(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_resource_task() -> list[str]:
    url = f"http://{METRICS_GEN_SERVICE_HOST}:{METRICS_GEN_SERVICE_PORT}/{METRICS_GEN_ENDPOINT}/"
    generated_data_portion_amount = 10

    async with aiohttp.ClientSession() as session:
        tasks = [get(session, url=url + str(num)) for num in range(generated_data_portion_amount)]
        raw_data = await asyncio.gather(*tasks)

    return raw_data
