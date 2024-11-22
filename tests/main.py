from typing import List

from pydantic import BaseModel

from snakifit import http_get, http_post, http_put, http_delete, http_host
from snakifit.handlers.request_handler import ApplicationJsonHandler, decorate_with_request_handlers


# Pydantic model for request validation
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(ItemCreate):
    id: int

@decorate_with_request_handlers(ApplicationJsonHandler)
@http_host("http://localhost:8999")
class MyHttpApiHost:
    
    @http_get('/items')
    def read_items(self) -> List[ItemResponse]:
        pass
    
    @http_post('/items')
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
    
    # @http_put('/WeatherForecast/{city}/{days}/{people}/fruit/{banana}')
    # def update_weather_forecast(self, city: str, days:int) -> dict:
    #     pass
    
api = MyHttpApiHost()
print(api.read_items())
print(api.http_host_info.__dict__)
