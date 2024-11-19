import functools
import logging

from snakifit.handlers.simple_delegate import SimpleDelegate
from snakifit.http_info import *

def _make_default_initializer(cls, base_url):
    
    def default_http_host_initializer(self, *args, **kwargs):
        if not hasattr(self, 'http_host_info'):
            self.http_host_info = HttpHostInfo()
        else:
            logging.warning(f'{self} already initialized as http host')
        
        real_base_url = ''
        if 'base_url' in kwargs:
            real_base_url = kwargs['base_url']
        else:
            real_base_url = base_url
        
        self.http_host_info.base_url = real_base_url
        
        for name, method in cls.__dict__.items():
            if callable(method) and hasattr(method, 'http_endpoint_info') and method.http_endpoint_info is not None:
                self.http_host_info.http_endpoints[name] = method.http_endpoint_info
                print(f"Decorating {name}")
        return self
    
    return default_http_host_initializer


def set_as_http_host(cls):
    if hasattr(cls, 'http_host_initialize_handler'):
        return cls
    
    original_init = cls.__init__
    cls.http_host_initialize_handler = SimpleDelegate()
    
    def new_init(self, *args, **kwargs):
        original_init(self)
        cls.http_host_initialize_handler.invoke(self, *args, **kwargs)
        # initialize_as_http_host(self)
    
    cls.__init__ = new_init
    return cls


def http_host(base_url: str = ""):
    def decorator(cls):
        set_as_http_host(cls)
        default_initializer = _make_default_initializer(cls, base_url)
        cls.http_host_initialize_handler += default_initializer
        return cls
    
    return decorator

def http_endpoint(method_name: str):
    def decorator(uri):
        def wrapper(func):
            http_endpoint_info = HttpEndpointInfo(method_name, uri)
            http_endpoint_info.check_path_params(func)
            func.http_endpoint_info = http_endpoint_info
            
            # return func
            @functools.wraps(func)
            def wrapped(api, *args, **kwargs):
                if hasattr(api, 'http_host_info'):
                    cls = api.__class__
                    if not hasattr(cls, 'http_host_initialize_handler'):
                        set_as_http_host(cls)
                        
                        # return _extract_and_send(
                #     method_name,
                #     api,
                #     uri,
                #     func,
                #     *args,
                #     **kwargs
                # )
            return wrapped
        
        return wrapper
    
    return decorator


# http_get = _http_endpoint("GET")
# http_post = _http_endpoint("POST")
# http_put = _http_endpoint("PUT")
# http_delete = _http_endpoint("DELETE")
# http_patch = _http_endpoint("PATCH")
# http_head = _http_endpoint("HEAD")
# http_options = _http_endpoint("OPTIONS")
# http_trace = _http_endpoint("TRACE")
# http_connect = _http_endpoint("CONNECT")
# 
# http_host = _http_host