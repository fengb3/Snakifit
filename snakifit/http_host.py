from snakifit.http_client import *


def http_host(base_url: str = ""):
    
    def decorator(cls):
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self._decorated_methods = {}
            for name, method in cls.__dict__.items():
                if callable(method) and hasattr(method, 'http_method_decorated') and method.http_method_decorated:
                    self._decorated_methods[name] = method
        
        cls.__init__ = new_init
        return cls
    
    return decorator
