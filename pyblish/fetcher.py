import asyncio
import random

class Fetcher: 
    @classmethod
    def producer_factory(cls, urls, documents):
        return [cls._produce(urls, documents) for _ in range(2)]

    async def _produce(urls, documents):
        for i in range(5):
            val = random.randint(1, 10)
            await asyncio.sleep(1)
            await documents.put(val)
            print('{} put a val: {}'.format(id, val))