import asyncio
import random
import logging
from aiohttp import ClientSession

logger = logging.getLogger(__name__)

class Fetcher: 
    @classmethod
    def factory(cls, urls):
        return [cls._fetch(urls) for _ in range(2)]

    async def _fetch(urls, **kwargs):
        while not urls.empty():
            url = urls.get_nowait()
            logger.info(f"got {url}")
            #resp = await session.request(method="GET", url=url, **kwargs)
            #resp.raise_for_status()
            #logger.info("Got response [%s] for URL: %s", resp.status, url)
            #html = await resp.text()
            #print(html)
            urls.task_done()
            #return html
