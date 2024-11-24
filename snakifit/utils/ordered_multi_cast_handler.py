import heapq
from typing import List, Callable


class OrderedMultiCastHandler:
    
    handlers: List[Callable]
    
    def __init__(self):
        self.handlers = []
        
    
    def invoke(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
        
    
    def add(self, other):
        if not callable(other):
            raise ValueError(f'{other} should be a callable')
        
        heapq.heappush(self.handlers, other)
    
    def remove(self, other):
        self.handlers.remove(other)
        
        
    def __iadd__(self, other):
        self.add(other)
        return self
    
    def __isub__(self, other):
        self.remove(other)
    
    def __call__(self, *args, **kwargs):
        self.invoke(*args, **kwargs)
            
    
        