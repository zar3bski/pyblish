import logging
import re
import hashlib
from asyncio import Queue
import urllib.error
import urllib.parse


logger = logging.getLogger(__name__)

class Parser:

    def __init__(self, root_url, url_to_parse:Queue) -> None:
        self.root_url = root_url
        self.url_to_parse = url_to_parse
        self.HREF_RE = re.compile(r'href="(.*?)"')
        self.parsed_internal = set()

    @classmethod
    def consumers_factory(cls, urls, documents):
        return [cls._consume(urls, documents) for _ in range(5)]

    async def parse(self, html_document):
        """
        Parse html, identify internal, external link and semantically meaningfull entities
        """
        found = set()
        html = await html_document
        html_hash = hashlib.sha256(html.encode('utf-8')).hexdigest()

        logger.info(f"doc {html_hash} consumed")
        for link in self.HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(self.root_url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
            else:
                found.add(abslink)
        
        found -= self.parsed_internal
        self.parsed_internal = self.parsed_internal.union(found)

        logger.info(f"doc {html_hash} found {found} new links" )
        for link in found:
            if link.startswith(self.root_url) and link.endswith(".html"):
                self.url_to_parse.put_nowait(link)

