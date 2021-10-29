import logging
import re
from asyncio import Queue, create_task, gather, ensure_future

class Parser: 

    def __init__(self, url_to_parse) -> None:
        self.url_to_parse = url_to_parse
        self.HREF_RE = re.compile(r'href="(.*?)"')

    @classmethod
    def consumers_factory(cls, urls, documents): 
        return [cls._consume(urls, documents)
                 for _ in range(5)]

    async def parse(html_document): 
        """
        Parse html, identify internal, external link and semantically meaningfull entities
        """
        while True:
            html = await documents.get()
            # process the token received from a producer
            
            #
            documents.task_done()
            logging.info(f'consumed document {html}')
