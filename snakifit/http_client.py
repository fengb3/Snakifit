import functools
import inspect
import logging
import re
from typing import Dict, get_type_hints, Callable, Union, List, get_origin, get_args

import httpx
from requests import Request, Session
from requests.exceptions import RequestException

from snakifit.http_info import *


# def http_host(_base_url: str = ""):
#     def decorator(cls):
#         # add properties to class marked by http_host decorator
#         cls._base_url = _base_url
#         cls.default_headers = {}
#         cls.enable_logging = True
#         cls.logger = logging.getLogger("http-client")
#         
#         def log_request(self, method: str, url: str, headers: dict, params: dict, data: Union[dict, None]):
#             if self.enable_logging:
#                 self.logger.info(
#                     f"Request - Method: {method}, URL: {url}, Headers: {headers}, Params: {params}, Data: {data}")
#         
#         def log_response(self, response):
#             if self.enable_logging:
#                 self.logger.info(f"with status code : {response.status_code} "
#                                  f"with content : {response.content}")
#         
#         cls.log_request = log_request
#         cls.log_response = log_response
#         
#         return cls
#     
#     return decorator

def _extract_and_send2(http_host, method_name, *args, **kwargs):
    
    http_host_info: HttpHostInfo = http_host.http_host_info
    http_endpoint_info: HttpEndpointInfo = http_host_info.http_endpoints[method_name]
    
    client = httpx.Client()
    
    url= http_host_info.base_url +'/' + http_endpoint_info.uri
    
    requests = httpx.Request(
        method = http_endpoint_info.http_method_name, 
        url = url
    )
    
    http_host_info.request_handlers.invoke(requests)
    http_endpoint_info.request_handlers.invoke(requests)
    
    pass


def _extract_and_send(method_name: str, api, uri: str, func: Callable, *args, **kwargs):
    """
    Extracts the parameters from the function and sends the request to the server.
        
    :param method_name: HTTP method can be GET, POST, PUT, DELETE, etc.
    :param api: the class_instance of the API class
    :param uri: the URI of the endpoint
    :param func: the function to be called
    :param args: 
    :param kwargs: 
    :return: 
    """
    signature = inspect.signature(func)
    bound_arguments = signature.bind(api, *args, **kwargs)
    bound_arguments.apply_defaults()
    param_types = get_type_hints(func)
    paths_keys = re.findall(r'{(.*?)}', uri)
    
    paths, queries, data = {}, {}, None
    
    for param_name, param_value in bound_arguments.arguments.items():
        if param_name == "self":
            continue
        
        param_type = param_types.get(param_name)
        if param_name in paths_keys:
            paths[param_name] = param_value
        elif param_name == "data":
            data = param_value.json() if hasattr(param_value, "json") else param_value
        elif param_type in [str, int, float, bool]:
            queries[param_name] = param_value
        else:
            api.logger.warning(f"Unknown parameter type: {param_type} in {func}")
    
    # Merge default headers with any provided headers
    headers = api.default_headers.copy()
    if 'headers' in kwargs:
        headers.update(kwargs['headers'])
    
    for key in paths:
        uri = uri.replace(f"{{{key}}}", str(paths[key]))
    
    url = api._base_url + uri
    
    # Check if path parameters are not replaced
    unfilled_path_params = re.findall(r'{(.*?)}', url)
    if unfilled_path_params:
        raise ValueError(f"Unfilled path parameters: {', '.join(unfilled_path_params)}")
    
    api.log_request(method_name, url, headers, queries, data)
    
    try:
        request = Request(
            method=method_name,
            url=url,
            params=queries,
            headers=headers,
            data=data
        )
        response = Session().send(request.prepare())
        # response = requests.request(method_name, _base_url, params=queries, headers=headers, data=data, timeout=100)
        api.log_response(response)
        response.raise_for_status()
    except RequestException as e:
        # self.logger.error(f"Request failed: {e}")
        api.logger.exception(f"Failed to send request to {url} "
                             f"with status code : {response.status_code} "
                             f"with content : {response.content}")
        return None
    
    return_type = param_types.get("return")
    if return_type is None:
        return None
    
    data_dict = response.json()
    
    # return return_type.parse_obj(response.json())
    
    # Check return type is a type that extends from BaseModel
    if hasattr(return_type, "parse_obj"):
        return return_type.parse_obj(data_dict)
    
    if get_origin(return_type) is list:
        inner_type = get_args(return_type)[0]
        if hasattr(inner_type, "parse_obj"):
            return [inner_type.parse_obj(item) for item in data_dict]
        else:
            return response.json()
    
    if return_type == str:
        return response.text
    
    if return_type == bytes:
        return response.content
    
    return data_dict

