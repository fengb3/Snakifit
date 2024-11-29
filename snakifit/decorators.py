# import functools
# import logging
# 
# from snakifit.helper.http_host_helper import set_as_http_host
# from snakifit.http_info import *
# 
# 
# def _make_default_initializer(cls, base_url):
#     def default_http_host_initializer(self, *args, **kwargs):
#         if not hasattr(self, 'http_host_info'):
#             self.http_host_info = HttpHostInfo()
#         else:
#             logging.warning(f'{self} already initialized as http host')
#         
#         real_base_url = ''
#         if '_base_url' in kwargs:
#             real_base_url = kwargs['_base_url']
#         else:
#             real_base_url = base_url
#         
#         self.http_host_info._base_url = real_base_url
#         
#         for name, method_name in cls.__dict__.items():
#             if callable(method_name) and hasattr(method_name, 'http_endpoint_info') and method_name.http_endpoint_info is not None:
#                 self.http_host_info.http_endpoints[name] = method_name.http_endpoint_info
#                 print(f"Decorating {name}")
#         return self
#     
#     return default_http_host_initializer
# 
# 
# def http_host(base_url: str = ""):
#     def decorator(cls):
#         set_as_http_host(cls)
#         default_initializer = _make_default_initializer(cls, base_url)
#         cls.http_host_initialize_handler += default_initializer
#         return cls
#     
#     return decorator
# 
# 
# def http_endpoint(method_name: str):
#     def decorator(uri):
#         def wrapper(func):
#             http_endpoint_info = HttpEndpointInfo(method_name, uri)
#             http_endpoint_info.check_path_params(func)
#             func.http_endpoint_info = http_endpoint_info
#             
#             # return func
#             @functools.wraps(func)
#             def wrapped(api, *args, **kwargs):
#                 if hasattr(api, 'http_host_info'):
#                     cls = api.__class__
#                     if not hasattr(cls, 'http_host_initialize_handler'):
#                         set_as_http_host(cls)
#                 
#                 # TODO: send
#                 # return 
#                 (
#                 #     method_name,
#                 #     api,
#                 #     uri,
#                 #     func,
#                 #     *args,
#                 #     **kwargs
#                 # )
#             
#             return wrapped
#         
#         return wrapper
#     
#     return decorator
import functools

from snakifit.helper.decorator_helper import make_parasite_decorator
from snakifit.http_info.http_fragment_node import add_http_fragment_node, HttpEndpointNode, send


def _http_host(base_url: str = ""):
    def add_http_host_node(target):
        node = add_http_fragment_node(target)
        node.uri_fragment = base_url
    
    return make_parasite_decorator(add_http_host_node)


def http_host(base_url: str = ""):
    return _http_host(base_url)


def _http_endpoint(method_name: str, uri: str):
    def add_http_endpoint_node(target):
        node: HttpEndpointNode = add_http_fragment_node(target)
        node.method = method_name
        node.uri = uri
    
    def wrapper(func):
        # @functools.wraps(func)
        def wrapped(*args, **kwargs):
            send(func.http_fragment_node)  # pass query params here
        
        return wrapped
    
    return make_parasite_decorator(add_http_endpoint_node, wrapper=wrapper)


def http_endpoint(method_name: str):
    def decorator(uri):
        return _http_endpoint(method_name, uri)
    
    return decorator
