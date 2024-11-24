import abc
import logging
import queue
import heapq
# from builtins import function
from typing import List, Callable, TypeVar, Generic, Type

import httpx

from snakifit.handlers.handler import PriorityHandler
from snakifit.helper.http_host_helper import set_as_http_host

# from snakifit.helper import set_as_http_host

T = TypeVar('T')


class RequestHandler(PriorityHandler[httpx.Request], abc.ABC):
    pass


class RequestLoggingHandler(RequestHandler):
    
    @property
    def priority(self):
        return 999
    
    def handle(self, request: httpx.Request, *args, **kwargs):
        logging.info(f"{request.method.to_upper()} '{request.url}' "
                     f"with data '{request.content}' "
                     f"with headers '{request.headers}' "
                     f"with queries '{request.url.params}'")


class ApplicationJsonHandler(RequestHandler):
    def handle(self, request: httpx.Request, *args, **kwargs):
        request.headers['Content-Type'] = 'application/json'
        
        
def decorate_with_request_handlers(*args):
    
    request_handlers = [each for each in args if issubclass(each, RequestHandler)]
    
    def decorator(cls):
        set_as_http_host(cls)
        for handler_type in request_handlers:
            handler_instance = handler_type()
            cls.http_host_initialize_handler += handler_instance
        return cls
    
    return decorator

# class RequestHandler(PriorityHandler, abc.ABC):
#     pass
# 
# 
# class RequestLoggingHandler(RequestHandler):
#     
#     @property
#     def priority(self):
#         return 999
#     
#     def handle(self, request : httpx.Request):
#         logging.info(f"{request.method.to_upper()} '{request.url}' "
#                      f"with data '{request.content}' "
#                      f"with headers '{request.headers}' "
#                      f"with queries '{request.url}'")
# 
# 
# class BuildUrlHandler(RequestHandler):
#     
#     def handle(self, request):
#         request.url = request.base_url + request.uri
#         for key in request.paths:
#             request.url = request.url.replace(f"{{{key}}}", request.paths[key])
# 
# 
# class ApplicationJsonHandler(RequestHandler):
#     
#     @property
#     def priority(self):
#         return 0
#     
#     def handle(self, request):
#         request.headers['Content-Type'] = 'application/json'
# 
# 
# class CustomHeaderHandler(RequestHandler):
#     def __init__(self, headers: dict):
#         self.headers = headers
#     
#     def handle(self, request):
#         request.headers.update(self.headers)
# 
# 
# def default_request_handlers() -> List[RequestHandler]:
#     handlers = [
#         ApplicationJsonHandler(),
#         RequestLoggingHandler()
#     ]
#     
#     handlers.sort(key=lambda x: x.priority, reverse=True)
#     
#     return handlers
