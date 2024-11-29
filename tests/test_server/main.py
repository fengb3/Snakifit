import logging

from fastapi import FastAPI, HTTPException, Request
# from fastapi.logger import logger
from pydantic import BaseModel
from typing import List

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch) #将日志输出至屏幕
logger.addHandler(fh) #将日志输出至文件

# In-memory database (dictionary)
database = {}
current_id = 1


# Pydantic model for request validation
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(ItemCreate):
    id: int

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def add_custom_log(request: Request, call_next):
    logger.info(f'headers: {request.headers}')
    response = await call_next(request)
    return response

@app.post("/test")
def test(request: Request):
    logger.info(f'headers: {request.headers}')
    
    # print out request details
    logger.info(f'headers: {request.headers}')
    logger.info(f'query_params: {request.query_params}')
    return {"msg": "ok"}

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    global current_id
    item_id = current_id
    database[item_id] = {"name": item.name, "description": item.description}
    current_id += 1
    return {"id": item_id, **database[item_id]}


@app.get("/items", response_model=List[ItemResponse])
def read_items():
    return [{"id": item_id, **data} for item_id, data in database.items()]


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **database[item_id]}


@app.get("/search/items", response_model=List[ItemResponse])
def search_item(search_keyword: str):
    # Perform a case-insensitive search
    results = [
        {"id": item_id, **data}
        for item_id, data in database.items()
        if search_keyword.lower() in data["name"].lower() or search_keyword.lower() in data["description"].lower()
    ]
    
    if not results:
        raise HTTPException(status_code=404, detail="No items found")
    
    return results


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[item_id] = {"name": item.name, "description": item.description}
    return {"id": item_id, **database[item_id]}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[item_id]
    return {"detail": "Item deleted"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8999)
