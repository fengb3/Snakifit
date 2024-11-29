from typing import Callable


def add_field_to_class_instance(cls, filed_name, field_value):
    
    if not isinstance(cls, type):
        raise ValueError(f'{cls.__name__} should be a class')
        
    original_init = cls.__init__
    
    def new_init(self, *args, **kwargs):
        original_init(self)
        setattr(self, filed_name, field_value)
    
    cls.__init__ = new_init
    

def add_field_to_function_instance(func, field_name, field_value):
    
    if not callable(func) and not isinstance(func, type):
        raise ValueError(f'{func.__name__} should be a function')
    
    def wrapper(*args, **kwargs):
        setattr(func, field_name, field_value)
        return func(*args, **kwargs)
    
    return wrapper


def add_field_to_method_instance(method, field_name, field_value):
    
    if not isinstance(method, classmethod):
        raise ValueError(f'{method.__name__} should be a method')
    
    def wrapper(self, *args, **kwargs):
        setattr(self, field_name, field_value)
        return method(self, *args, **kwargs)
    
    return wrapper

def _plain_wrapper(target):
    return target

def make_parasite_decorator(*args, **kwargs):
    
    # 检查是否有wrapper参数，如果有就使用它，否则使用默认的wrapper
    wrapper = kwargs.get('wrapper', _plain_wrapper)
    
    def decorator(target):
        
        # 遍历所有的参数，如果是可执行的，就执行它
        for parasite_operation in filter(lambda op: callable(op), args):
            parasite_operation(target) # 执行操作
        
        return wrapper(target) # 返回装饰器
    
    return decorator