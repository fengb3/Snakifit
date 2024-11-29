import inspect
from typing import List, Union, Callable
import re

import httpx

from snakifit.handlers.ordered_multi_cast_handler import OrderedMultiCastHandler
from snakifit.helper.decorator_helper import make_parasite_decorator
from snakifit.http_info.http_context import HttpContext
from snakifit.utils.double_linked_multi_tree import DoubleLinkedMultiTree
from snakifit.handlers.multi_cast_delegate import MultiCastDelegate


class HttpFragmentNode(DoubleLinkedMultiTree):
    
    def __init__(self, parent=None, value=None):
        super().__init__(parent=parent, value=value)
        self._uri_fragment = ''
        self._request_handler = MultiCastDelegate()
        self._response_handler = MultiCastDelegate()
    
    @property
    def uri_fragment(self):
        return self._uri_fragment
    
    @uri_fragment.setter
    def uri_fragment(self, uri_fragment):
        # remove ending slash if there is any
        self._uri_fragment = uri_fragment.rstrip('/')
    
    @property
    def request_handler(self):
        return self._request_handler
    
    @request_handler.setter
    def request_handler(self, request_handler):
        self._request_handler = request_handler
    
    @property
    def response_handler(self):
        return self._response_handler
    
    @response_handler.setter
    def response_handler(self, response_handler):
        self._response_handler = response_handler


class HttpHostNode(HttpFragmentNode):
    
    @property
    def base_url(self):
        return self.uri_fragment
    
    @base_url.setter
    def base_url(self, base_url):
        self.uri_fragment = base_url


class HttpEndpointNode(HttpFragmentNode):
    
    def __init__(self, parent=None, value=None):
        super().__init__(parent=parent, value=value)
        self._method: str = ''
        self._path_keys: List[str] = []
        # node.path_keys = re.findall(r'{(.*?)}', uri)


    @property
    def method(self):
        return self._method
    
    @method.setter
    def method(self, method_name: str):
        self._method = method_name.upper()
        
    @property
    def uri(self):
        return self._uri_fragment
    
    @uri.setter
    def uri(self, value: str):
        self._uri_fragment = value.rstrip('/')
        self._path_keys = re.findall(r'{(.*?)}', value)
    
    def check_path_params(self, func: Callable):
        """检查函数的参数是否包含所有的path参数"""
        signature = inspect.signature(func)
        param_names = list(signature.parameters.keys())
        missing_params = []
        for key in self.path_keys:
            if key not in param_names:
                missing_params.append(key)
        if missing_params:
            raise ValueError(f"Missing path parameter(s) '{', '.join(missing_params)}' in function {func.__name__}")



def add_http_fragment_node(target) -> Union[HttpEndpointNode, HttpHostNode]:
    # check target has node or not
    if hasattr(target, 'http_fragment_node') and target.http_fragment_node is not None:
        return target.http_fragment_node
    
    # check target's type, if it is a class add HttpHostNode
    # if it is a method_name add HttpEndpointNode
    if isinstance(target, type):
        cur_node = HttpHostNode(value=target)
    else:
        cur_node = HttpEndpointNode(value=target)
    
    target.http_fragment_node = cur_node
    
    for name, item in target.__dict__.items():
        if hasattr(item, 'http_fragment_node') and item.http_fragment_node is not None:
            item.http_fragment_node.parent = cur_node
    
    return cur_node
    
def send(node: HttpEndpointNode):
    """发送请求"""
    # Traverse from the current node to the parent to get all the nodes along the way
    nodes = []
    cur_node = node
    while cur_node:
        nodes.append(cur_node)
        cur_node = cur_node.parent
    
    # loop through the nodes to get the url and handlers
    url = ''
    request_handler = OrderedMultiCastHandler()
    response_handler = OrderedMultiCastHandler()
    
    http_context = HttpContext()
    
    while len(nodes) > 0:
        cur_node = nodes.pop()
        url += cur_node.uri_fragment
        request_handler += cur_node.request_handler
        response_handler += cur_node.response_handler
    
    # print(f"Sending request to {url} with method_name {node.method_name}")
    
    request = httpx.Request(url=url, method=node.method)
    client = httpx.Client()
    # 
    request_handler(request)
    #     
    response = client.send(request)
    # 
    response_handler(response)
    
    pass


def loging_request_handler():
    print('loging_request_handler called')
    
    def handler(request):
        print(f"Requesting {request.url} with method {request.method}")
    
    def add_request_handler(target):
        # print('add_logging_request_handler called')
        target.node.request_handler += handler
    
    return make_parasite_decorator(add_request_handler)

# test code below
# @loging_request_handler()
# @http_host('http://localhost:8000')
# class TestApi:
#     
#     @get('/test')
#     def test(node):
#         print('test')
#     
#     @post('/test')
#     def test_post(node):
#         print('test post')
# 
# 
# if __name__ == '__main__':
#     api = TestApi()
#     api.test()
