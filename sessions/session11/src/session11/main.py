from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# simular base de dados
items = {
    1: {"name": "item1", "price": 100},
    2: {"name": "item2", "price": 200}
}

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
async def read_root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the FastAPI API!"}

@app.get("/items/{item_id}")
async def get_items(item_id: int):
    if item_id in items:
        return {"item": items[item_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
async def create_item(item: Item):
    if "name" not in item:
        logger.info(f"Item received: {item}")
        new_item_id = max(items.keys(), default=0) + 1  
        items[new_item_id] = item.model_dump()  
        logger.info(f"Item added: {item}")
        return {"item": item}
    else:
        logger.error("Item does not contain 'name'")
        raise HTTPException(status_code=400, detail="Item must have a name")

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id in items:
        items[item_id] = item.model_dump()  
        return {"message": "Item updated successfully", "item": items[item_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in items:
        items[item_id] = None
        return {"message": "Item deleted successfully", "item": None}
    else:
        raise HTTPException(status_code=404, detail="Item not found")