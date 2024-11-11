import abc

from typing import Callable, Generic, TypeVar, List, Union, Dict, Any, Tuple, Optional, Type, get_type_hints, \
    get_origin, get_args


class Delegate(abc.ABC):
    def __init__(self):
        self._delegates: List[Callable] = []
    
    def add(self, callback: Callable):
        self._delegates.append(callback)
    
    def invoke(self, *args, **kwargs):
        for callback in self._delegates:
            callback(*args, **kwargs)


T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
T8 = TypeVar('T8')

class Action(Generic[T1, T2, T3, T4, T5, T6, T7, T8], Delegate):
    def __init__(self, *args: Any):
        super().__init__()
        self.arg_types = {}
        for i, arg in enumerate(args):
            self.arg_types[i] = type(arg)
    


inst = Action[int, str](1, "hello")
inst2 = Action[int](1)

print(inst.arg_types)
print(inst2.arg_types)