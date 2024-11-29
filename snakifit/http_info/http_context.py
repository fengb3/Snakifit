# 
from typing import List, Dict

import httpx
from httpx import Request, Response
from pydantic import BaseModel

from snakifit.handlers.multi_cast_delegate import MultiCastDelegate
from snakifit.handlers.ordered_multi_cast_handler import OrderedMultiCastHandler


class HttpContext:
    method_name: str
    query_params: Dict
    raw_url: str = None
    path_params = {}
    
    request: Request = None
    response: Response = None
    
    _request_handler: OrderedMultiCastHandler
    _response_handler: OrderedMultiCastHandler
    
    _client: httpx.Client = None

    def __init__(self):
        self._request_handler = OrderedMultiCastHandler()
        self._response_handler = OrderedMultiCastHandler()
        self.query_params = {}
        self.path_params = {}
        self.method_name = ''
        
