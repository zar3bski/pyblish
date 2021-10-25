import asyncio
import argparse
from asyncio import Queue
import random
from pyblish.fetcher import Fetcher

from pyblish.parser import Parser


async def producer(queue, id):
    for i in range(5):
        val = random.randint(1, 10)
        await asyncio.sleep(1)
        await queue.put(val)
        print('{} put a val: {}'.format(id, val))


async def main():
    url_to_parse = asyncio.Queue()
    html_documents = asyncio.Queue()

    producers = Fetcher.producer_factory(url_to_parse, html_documents)
    consumers = Parser.consumers_factory(url_to_parse, html_documents)

    await asyncio.gather(*producers, return_exceptions=True)
    await asyncio.gather(*consumers, return_exceptions=True)
    


    await html_documents.join()
    await url_to_parse.join()  # wait until the consumer has processed all items
    
    for consumer in consumers: 
        consumer.cancel()
    for producer in producers: 
        producer.cancel()


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Analyse website content')
    parser.add_argument('root_url', help="Root url of the website")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close() 