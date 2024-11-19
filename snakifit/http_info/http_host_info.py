from typing import Dict

from snakifit.handlers.simple_delegate import SimpleDelegate
from .http_endpoint_info import HttpEndpointInfo


class HttpHostInfo:
    http_endpoints: Dict[str, HttpEndpointInfo]
    base_url: str
    request_handlers: SimpleDelegate
    response_handlers: SimpleDelegate
    
    def __init__(self):
        self.request_handlers = SimpleDelegate()
        self.response_handlers = SimpleDelegate()
        self.http_endpoints = {}
        self.base_url = ""