import asyncio
import random
import logging
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class Fetcher:
    @classmethod
    def factory(cls, urls, parser):
        return [cls._fetch(i, urls, parser) for i in range(2)]

    async def _fetch(worker_nb, urls, parser, **kwargs):
        async with ClientSession() as session:
            while not urls.empty():
                url = urls.get_nowait()
                logger.info(f"worker_{worker_nb} got {url}")
                resp = await session.request(method="GET", url=url, **kwargs)
                resp.raise_for_status()
                logger.info(f"Got response {resp.status} for URL: {url}")
                html = await resp.text()
                print(html)
                urls.task_done()
            # return html
