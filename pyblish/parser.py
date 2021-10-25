import logging
from asyncio import Queue, create_task, gather, ensure_future

class Parser: 

    @classmethod
    def consumers_factory(cls, urls, documents): 
        return [cls._consume(urls, documents)
                 for _ in range(5)]

    async def _consume(urls, documents): 
        """
        Parse html, identify internal, external link and semantically meaningfull entities
        """
        while True:
            html = await documents.get()
            # process the token received from a producer
            
            #
            documents.task_done()
            logging.info(f'consumed document {html}')
