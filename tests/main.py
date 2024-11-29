from typing import List

from pydantic import BaseModel

from snakifit import *


# Pydantic model for request validation
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(ItemCreate):
    id: int


# @decorate_with_request_handlers(ApplicationJsonHandler)
@http_host("http://localhost:8999")
class MyHttpApiHost:
    
    @http_get('/items')
    def read_items(self) -> List[ItemResponse]:
        pass
    
    @http_post('/items')
    def create_item(self, item: ItemCreate) -> ItemResponse:
        pass
    
    @http_get('/search/items')
    def search_item(self, search_keyword: str) -> List[ItemResponse]:
        pass
    
    @http_put('/items/{item_id}')
    def update_item(self, item_id: int, item: ItemCreate) -> List[ItemResponse]:
        pass
    
    @http_delete('/items/{item_id}')
    def delete_item(self, item_id):
        pass
    
    @http_post('/test')
    def test1(self):
        pass
    
    @http_post('/test')
    def test2(self, some_str: str, some_int: int):
        pass


api = MyHttpApiHost()
print(api.test2("str",2, False))
# print(api.__dict__)
