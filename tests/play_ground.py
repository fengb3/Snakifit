import builtins
import functools
from typing import Callable

class DoubleLinkedMultiTree:
    def __init__(self, parent: 'DoubleLinkedMultiTree' = None, value = None):
        self._parent = parent
        self._children = []
        self._value = value
        
    @property
    def parent(self) -> 'DoubleLinkedMultiTree':
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        self._parent = parent
        if parent:
            parent.children.append(self)
            
    @property
    def children(self) -> list['DoubleLinkedMultiTree']:
        return self._children
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        
    def __repr__(self, level=0):
        ret = "\t" * level + repr(self._value.__name__)+"\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
    

class Parasite:
        
    def __init__(self, target: type | classmethod):
        self.target = target   
        cur_node = DoubleLinkedMultiTree(value=target)
        self.node = cur_node
        
        if isinstance(target, Callable) and not isinstance(target, type):
            print(f'adding Parasite to a func {target.__name__}')
   
        if isinstance(target, type):
            print(f'adding Parasite to a class {target.__name__}')
            
        for name, method in target.__dict__.items():
            if callable(method) and hasattr(method, 'node') and method.node is not None:
                print(f'find a method {name} with node under {target.__name__}')
                method.node.parent = cur_node
        # else:
        #     raise ValueError(f'Invalid value type {value}')
        
        functools.update_wrapper(self, target)
       
    
    def __call__(self, *args, **kwargs):    
        print(f'calling {self.target.__name__}')
        return self.target(*args, **kwargs)
    
    # def __get__(self, instance, owner):
    #     return functools.partial(self, instance)



@Parasite
class TestClass:
    
    @Parasite
    def test_function(self):
        print("calling test function")
        
    
    @Parasite
    def test_function2(self):
        print("calling test function2")
        
    
    @Parasite
    class TestInnerClass:
        
        @Parasite
        def test_inner_function(self):
            print("calling test inner function")


# class DoubleLinkedMultiTree:
#     def __init__(self, name, node_type):
#         self.name = name
#         self.node_type = node_type
#         self.children = []
#     
#     def add_child(self, child):
#         self.children.append(child)
#     
#     def __repr__(self, level=0):
#         ret = "\t" * level + repr(self.name) + " (" + self.node_type + ")\n"
#         for child in self.children:
#             ret += child.__repr__(level + 1)
#         return ret
# 
# 
# def build_tree(cls, parent_node=None):
#     if parent_node is None:
#         parent_node = DoubleLinkedMultiTree(cls.__name__, "class")
#     
#     for name, obj in cls.__dict__.items():
#         if isinstance(obj, type):
#             child_node = DoubleLinkedMultiTree(name, "class")
#             parent_node.add_child(child_node)
#             build_tree(obj, child_node)
#         elif callable(obj):
#             child_node = DoubleLinkedMultiTree(name, "method")
#             parent_node.add_child(child_node)
#     
#     return parent_node

print('1')
class_instance = TestClass()
gg = class_instance.test_function
gg2 = class_instance.test_function2
print('2')

print(TestClass.node)



