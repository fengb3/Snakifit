import abc
import heapq
from typing import *

T = TypeVar('T')


class PriorityHandler(Generic[T], abc.ABC, Callable):
    
    def __call__(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
    
    @abc.abstractmethod
    def handle(self, t: T, *args, **kwargs):
        pass
    
    @property
    def priority(self):
        return 10
    
    def __lt__(self, other):
        if not hasattr(other, 'priority'):
            return False # other is always less than self
        return self.priority < other.priority


class HandlerHolder(Generic[T]):
    handlers_heap: List[PriorityHandler[T]]
    
    def __init__(self):
        self.handlers_heap = []
    
    def __add__(self, other):
        if isinstance(other, PriorityHandler):
            heapq.heappush(self.handlers_heap, other)
        elif isinstance(other, HandlerHolder):
            for handler in other.handlers_heap:
                heapq.heappush(self.handlers_heap, handler)
        elif isinstance(other, Callable):
            class TempHandler(PriorityHandler):
                def handle(self, t: T, *args, **kwargs):
                    other(t, *args, **kwargs)
            
            heapq.heappush(self.handlers_heap, TempHandler())
        else:
            raise TypeError(f"Unsupported type {type(other)}")
        
        return self
    
    def __sub__(self, other):
        if isinstance(other, PriorityHandler):
            self.handlers_heap.remove(other)
        elif isinstance(other, HandlerHolder):
            for handler in other.handlers_heap:
                self.handlers_heap.remove(handler)
        else:
            raise TypeError(f"Unsupported type {type(other)}")
        
        return self
    
    def __call__(self, param: T, *args, **kwargs):
        for handler in self.handlers_heap:
            handler.handle(param, *args, **kwargs)
    
    def invoke(self, param: T, *args, **kwargs):
        self.__call__(param, *args, **kwargs)