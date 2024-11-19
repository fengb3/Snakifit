import inspect
from typing import List, Dict, Callable
import re


class HttpEndpointInfo:
    uri: str
    http_method_name: str
    path_keys: List[str]
    args: List[str]
    kwargs: Dict[str, str]
    
    def __init__(self, http_method_name: str, uri: str = ""):
        self.http_method_name = http_method_name.upper()
        self.uri = uri
        self.path_keys = re.findall(r'{(.*?)}', uri)
    
    def check_path_params(self, func: Callable):
        """检查函数的参数是否包含所有的path参数"""
        signature = inspect.signature(func)
        param_names = list(signature.parameters.keys())
        missing_params = []
        for key in self.path_keys:
            if key not in param_names:
                missing_params.append(key)
        if missing_params:
            raise ValueError(f"Missing path parameter(s) '{', '.join(missing_params)}' in function {func.__name__}")
