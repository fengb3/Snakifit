from typing import Dict

from snakifit.handlers.simple_delegate import SimpleDelegate
from .http_endpoint_info import HttpEndpointInfo


class HttpHostInfo:
    http_endpoints: Dict[str, HttpEndpointInfo]
    _base_url: str
    request_handlers: SimpleDelegate
    response_handlers: SimpleDelegate
    
    def __init__(self):
        self.request_handlers = SimpleDelegate()
        self.response_handlers = SimpleDelegate()
        self.http_endpoints = {}
        self._base_url = ""
        
    @property
    def base_url(self):
        return self._base_url
    
    @base_url.setter
    def base_url(self, value):
        self._base_url = value.lsstrip("/")