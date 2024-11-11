import abc
import logging
from typing import List, Callable
from requests import Response, Request

from snakifit.request_builder import RequestDatas


class Handler(abc.ABC):
    def handle(self, res):
        pass
    
    @property
    def priority(self):
        return 10


class RequestHandler(Handler, abc.ABC):
    pass


class RequestLoggingHandler(RequestHandler):
    
    @property
    def priority(self):
        return 999
    
    def handle(self, request):
        logging.info(f"{request.method.to_upper()} '{request.url}' "
                     f"with data '{request.data}' "
                     f"with headers '{request.headers}' "
                     f"with queries '{request.params}'")


class BuildUrlHandler(RequestHandler):
    
    def handle(self, request):
        request.url = request.base_url + request.uri
        for key in request.paths:
            request.url = request.url.replace(f"{{{key}}}", request.paths[key])


class ApplicationJsonHandler(RequestHandler):
    
    @property
    def priority(self):
        return 0
    
    def handle(self, request):
        request.headers['Content-Type'] = 'application/json'


class CustomHeaderHandler(RequestHandler):
    def __init__(self, headers: dict):
        self.headers = headers
    
    def handle(self, request):
        request.headers.update(self.headers)


def default_request_handlers() -> List[RequestHandler]:
    handlers = [
        ApplicationJsonHandler(),
        RequestLoggingHandler()
    ]
    
    handlers.sort(key=lambda x: x.priority, reverse=True)
    
    return handlers
