from pydantic import BaseModel

from snakifit.http_client import *
from snakifit.http_host import http_host


# Pydantic model for request validation
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(ItemCreate):
    id: int

@http_host("http://localhost:8999")
class MyHttpApiHost:
    
    @http_get('/items')
    def read_items(self) -> List[ItemResponse]:
        pass
    
    @http_post('/items/{item_id}')
    def create_item(self, item: ItemCreate) ->ItemResponse:
        pass
    
    @http_get('/search/items')
    def search_item(self, search_keyword:str)->List[ItemResponse]:
        pass
    
    @http_put('/items/{item_id}')
    def update_item(self, item_id:int, item: ItemCreate) -> List[ItemResponse]:
        pass
    
    @http_delete('/items/{item_id}')
    def delete_item(self, item_id):
        pass
    
api = MyHttpApiHost()
print(api.__dict__)