from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# In-memory database (dictionary)
database = {}
current_id = 1


# Pydantic model for request validation
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(ItemCreate):
    id: int


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
