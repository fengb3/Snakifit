from . import decorators

# __all__ = [
#     'http_get',
#     'http_post',
# ]

http_get = decorators.http_endpoint("GET")
http_post = decorators.http_endpoint("POST")
http_put = decorators.http_endpoint("PUT")
http_delete = decorators.http_endpoint("DELETE")
http_patch = decorators.http_endpoint("PATCH")
http_head = decorators.http_endpoint("HEAD")
http_options = decorators.http_endpoint("OPTIONS")
http_trace = decorators.http_endpoint("TRACE")
http_connect = decorators.http_endpoint("CONNECT")

http_host = decorators.http_host
