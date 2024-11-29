import functools
from typing import List, Union

import httpx

from snakifit.helper.decorator_helper import parasite
from snakifit.utils.double_linked_multi_tree import DoubleLinkedMultiTree
from multi_cast_delegate import MultiCastDelegate


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
        self._uri_fragment = uri_fragment
    
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
        return self._uri_fragment
    
    @base_url.setter
    def base_url(self, base_url):
        self._uri_fragment = base_url


class HttpEndpointNode(HttpFragmentNode):
    
    def __init__(self, parent=None, value=None):
        super().__init__(parent=parent, value=value)
        self._method = ''
        self._path_keys: List[str]
    
    @property
    def method(self):
        return self._method
    
    @method.setter
    def method(self, method):
        self._method = method
    
    def send(self):
        """发送请求"""
        # 从当前节点向父级遍历，获取一路上的所有节点
        nodes = []
        cur_node = self
        while cur_node:
            nodes.append(cur_node)
            cur_node = cur_node.parent
        
        url = ''
        request_handler = MultiCastDelegate()
        response_handler = MultiCastDelegate()
        
        while len(nodes) > 0:
            cur_node = nodes.pop()
            url += cur_node.uri_fragment
            request_handler += cur_node.request_handler
            response_handler += cur_node.response_handler
        
        # print(f"Sending request to {url} with method {self.method}")
        
        request = httpx.Request(url=url, method=self.method)
        client = httpx.AsyncClient()
        # 
        request_handler(request)
        #     
        # response = client.send(request)
        # 
        # response_handler(response)
        
        pass
    
    
def add_http_fragment_node(target) -> Union[HttpEndpointNode, HttpHostNode]:
    
    # check target has node or not
    if hasattr(target, 'http_fragment_node') or target.http_fragment_node is not None:
        return target.http_fragment_node
    
    # check target's type, if it is a class add HttpHostNode
    # if it is a method add HttpEndpointNode
    if isinstance(target, type):
        cur_node = HttpHostNode(value=target)
    else:
        cur_node = HttpEndpointNode(value=target)
        
    target.http_fragment_node = cur_node
    
    for name, item in target.__dict__.items():
        if hasattr(item, 'http_fragment_node') and item.http_fragment_node is not None:
            item.http_fragment_node.parent = cur_node
            
    return cur_node


# def http_host(base_url: str = ""):
#     print('http_host called')
#     
#     def add_http_host_node(target):
#         # print('add_http_host_node called')
#         # cur_node = HttpHostNode(value=target)
#         # cur_node.base_url = base_url
#         # target.node = cur_node
#         # 
#         # for name, item in target.__dict__.items():
#         #     if hasattr(item, 'node') and item.node is not None:
#         #         # print(f'{name} has node on it')
#         #         item.node.parent = cur_node
#         node = add_http_fragment_node(target)
#         node.uri_fragment = base_url
#         
#     
#     return parasite(add_http_host_node)


# def http_endpoint(method_name: str, uri: str):
#     def add_http_endpoint_node(target):
#         # cur_node = HttpEndpointNode(value=target)
#         # cur_node.method = method_name
#         # cur_node.uri_fragment = uri
#         # target.node = cur_node
#         node = add_http_fragment_node(target) 
#         node.method = method_name
#         node.uri_fragment = uri
#     
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapped(*args, **kwargs):
#             func.node.send()
#         
#         return wrapped
#     
#     return parasite(add_http_endpoint_node, wrapper=decorator)


# def http_method_wrapper(method_name: str):
#     def decorator(uri):
#         # return http_endpoint(method_name, uri)
#         pass
#     
#     return decorator
# 
# 
# get = http_method_wrapper('GET')
# post = http_method_wrapper('POST')
# put = http_method_wrapper('PUT')
# delete = http_method_wrapper('DELETE')
# patch = http_method_wrapper('PATCH')
# options = http_method_wrapper('OPTIONS')
# head = http_method_wrapper('HEAD')
# trace = http_method_wrapper('TRACE')
# connect = http_method_wrapper('CONNECT')


def loging_request_handler():
    print('loging_request_handler called')
    
    def handler(request):
        print(f"Requesting {request.url} with method {request.method}")
    
    def add_request_handler(target):
        #print('add_logging_request_handler called')
        target.node.request_handler += handler
    
    return parasite(add_request_handler)


# test code below
# @loging_request_handler()
# @http_host('http://localhost:8000')
# class TestApi:
#     
#     @get('/test')
#     def test(self):
#         print('test')
#     
#     @post('/test')
#     def test_post(self):
#         print('test post')
# 
# 
# if __name__ == '__main__':
#     api = TestApi()
#     api.test()
