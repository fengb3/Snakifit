import abc
from typing import TypeVar, Generic, Callable, List, overload


class SimpleDelegate:
    """A simple delegate class that can hold multiple request_handlers"""
    
    def __init__(self):
        self.handlers = []
    
    def __add__(self, other):
        if isinstance(other, SimpleDelegate):
            print("Adding delegate")
            self.handlers.extend(other.handlers)
        elif isinstance(other, Callable):
            print("Adding handler")
            self.handlers.append(other)
        else:
            raise TypeError(f"Unsupported type {type(other)}")
        
        return self
    
    def __sub__(self, other):
        pass
    
    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
    
    def invoke(self, *args, **kwargs):
        self.__call__(*args, **kwargs)

