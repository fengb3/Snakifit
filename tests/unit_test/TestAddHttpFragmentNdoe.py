import unittest

from snakifit import http_host, http_get, http_post
from snakifit.http_info.http_fragment_node import add_http_fragment_node, HttpHostNode, HttpEndpointNode


# class TestHttpDecorator():

class TestAddHttpFragmentNode(unittest.TestCase):
    
    class TestClass:
        pass
    
    def test_add_http_fragment_node_to_class(self):
        target = self.TestClass
        node = add_http_fragment_node(target)
        self.assertIsInstance(node, HttpHostNode)
        self.assertEqual(node, target.http_fragment_node)
    
    def test_add_http_fragment_node_to_method(self):
        def test_method():
            pass
        
        node = add_http_fragment_node(test_method)
        self.assertIsInstance(node, HttpEndpointNode)
        self.assertEqual(node, test_method.http_fragment_node)
    
    def test_add_http_fragment_node_to_class_with_existing_node(self):
        target = self.TestClass()
        existing_node = HttpHostNode(value=target)
        target.http_fragment_node = existing_node
        
        node = add_http_fragment_node(target)
        self.assertEqual(node, existing_node)
    
    def test_add_http_fragment_node_to_method_with_existing_node(self):
        def test_method():
            pass
        
        existing_node = HttpEndpointNode(value=test_method)
        test_method.http_fragment_node = existing_node
        
        node = add_http_fragment_node(test_method)
        self.assertEqual(node, existing_node)
        
class TestHttpDecorator(unittest.TestCase):
    
    @http_host('http://localhost')
    class TestClass:
        
        @http_get('/test')
        def test(self):
            pass
        
        @http_host('/gg')
        class TestInnerClass:
            
            @http_post('/test')
            def test(self):
                pass
    
    def test_decorate_http_host(self):
        cls = self.TestClass
        
        self.assertIsInstance(cls.http_fragment_node, HttpHostNode)
        self.assertEqual(cls.http_fragment_node.value, cls)
        self.assertEqual(cls.http_fragment_node.base_url, 'http://localhost')
        
    
    def test_decorate_inner_http_host(self):
        cls = self.TestClass.TestInnerClass
        
        self.assertIsInstance(cls.http_fragment_node, HttpHostNode)
        self.assertEqual(cls.http_fragment_node.value, cls)
        self.assertEqual(cls.http_fragment_node.base_url, '/gg')
        
    def test_decorate_http_endpoint(self):
        func = self.TestClass.test
        
        self.assertIsInstance(func.http_fragment_node, HttpEndpointNode)
        self.assertEqual(func.http_fragment_node.method, 'GET')
        self.assertEqual(func.http_fragment_node.uri, '/test')

if __name__ == '__main__':
    unittest.main()
