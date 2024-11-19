import unittest
from typing import Callable
from snakifit.handlers.simple_delegate import SimpleDelegate

class TestSimpleDelegate(unittest.TestCase):
    def test_add_handler(self):
        delegate = SimpleDelegate()
        def say_something(something: str):
            print(something)
            
        delegate += say_something
        
        self.assertEqual(len(delegate.handlers), 1)
        
        delegate.invoke("Hello")

    def test_add_delegate(self):
        delegate1 = SimpleDelegate()
        delegate2 = SimpleDelegate()
        
        def say_something(something: str):
            print(something)
            
        delegate1 += say_something
        
        delegate2 += delegate1
        
        self.assertEqual(len(delegate2.handlers), 1)
        
        delegate2.invoke("Hello")
        
    def test_operate_reference_type(self):
        delegate = SimpleDelegate()
        
        class ReferenceType:
            def __init__(self):
                self.value = 0
                
            def increase(self):
                self.value += 1
                
        reference = ReferenceType()
        
        delegate += reference.increase
        
        delegate.invoke()
        
        self.assertEqual(reference.value, 1)
        

# if __name__ == '__main__':
#     unittest.main()