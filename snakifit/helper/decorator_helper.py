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

def parasite(*args, **kwargs):
    
    if 'wrapper' in kwargs:
        wrapper = kwargs['wrapper']
    else:
        wrapper = lambda target: target
    
    def decorator(target):
        
        for operation in args:
            
            if not isinstance(operation, Callable):
                continue
            
            operation(target)
        
        return wrapper(target)
    
    return decorator