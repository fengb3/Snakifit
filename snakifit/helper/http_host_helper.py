from snakifit.handlers import HandlerHolder


def set_as_http_host(cls):
    if hasattr(cls, 'http_host_initialize_handler'):
        return cls
    
    original_init = cls.__init__
    cls.http_host_initialize_handler = HandlerHolder()
    
    def new_init(self, *args, **kwargs):
        original_init(self)
        cls.http_host_initialize_handler.invoke(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls