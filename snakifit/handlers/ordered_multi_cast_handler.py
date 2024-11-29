import heapq
from typing import List, Callable

from snakifit.handlers.delegate import Delegate
from snakifit.handlers.multi_cast_delegate import MultiCastDelegate


class OrderedMultiCastHandler(MultiCastDelegate):
    
    priority: int
    """调用优先级"""
    
    def invoke(self, *args, **kwargs):
        pass
    
    def __init__(self, priority: int = 0):
        super().__init__()
        self.priority = priority
    
    def add(self, other):
        if not callable(other):
            raise ValueError(f'{other} should be a callable')
        
        heapq.heappush(self.delegates, other)
    
    def __lt__(self, other):
        
        if hasattr(other, 'priority') and other.priority is not None:
            return self.priority < other.priority
        
        return False
