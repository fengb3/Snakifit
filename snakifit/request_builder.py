from typing import Optional

from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()
    CONNECT = auto()
    OPTIONS = auto()
    TRACE = auto()


class RequestDatas:
    http_method: Optional[HttpMethod] = None
    paths: dict = {}
    uri: Optional[str] = None
    queries: dict = {}
    headers: dict = {}
    body: Optional[dict] = None
    files: Optional[dict] = None
    
    def with_http_method(self, http_method: HttpMethod):
        self.http_method = http_method
        return self
    
    def with_uri(self, uri: str):
        self.uri = uri
        return self
    
    def with_queries(self, queries: dict):
        self.queries = queries
        return self
    
    def add_query(self, k: str, v: str):
        self.queries[k] = v
        return self
    
    def with_headers(self, headers: dict):
        self.headers = headers
        return self
    
    def add_header(self, k: str, v: str):
        self.headers[k] = v
        return self
    
    def with_body(self, body: dict):
        self.body = body
        return self
    
    def with_files(self, files: dict):
        self.files = files
        return self
    
    # def build_url(self, domain: str):
    #     if self.paths is None:
    #         self.paths = {}
    #     for key in self.paths:
    #         self.uri = self.uri.replace(f"{{{key}}}", self.paths[key])
    #         
    #     #handle tailing '/' in domain and leading '/' in uri        
    #     while domain[-1] == '/':
    #         domain = domain[:-1]
    #     
    #     while self.uri[0] == '/':
    #         self.uri = self.uri[1:]
    #         
    #     return f'{domain}/{self.uri}'
    
    