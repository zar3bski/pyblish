import asyncio
import argparse
from asyncio import Queue
import random
import logging

from aiohttp.client import ClientSession
from pyblish.fetcher import Fetcher

from pyblish.parser import Parser


logger = logging.getLogger(__name__)
ARGS = argparse.ArgumentParser(description='Analyse website content')
ARGS.add_argument('root_url', help="Root url of the website")

def main():
    logging.basicConfig(level=logging.INFO)
    args = ARGS.parse_args()

    url_to_parse = Queue()
    logger.info(f"Running main on {args.root_url}")
    url_to_parse.put_nowait(args.root_url)
    
    parser = Parser(args.root_url, url_to_parse)
    fetchers = Fetcher.factory(url_to_parse, parser)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(fetchers))
    loop.close()


if __name__ == "__main__": 
    main()
