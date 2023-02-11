from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None #always default optional values

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get('/')
def home():
    return {"Data": "Test"}

@app.get('/about')
def about():
    return {"Data": "About"}

# notice that there is a difference between objects and dictionaries. Duh but this is a bit different than JS.
# inventory = {
#     1: {
#         "name": "Milk",
#         "price": 3.99,
#         "brand": "Regular"
#     }
# }
inventory = {
    1: Item(name = "Milk", price = 3.99, brand = "Regular")
}

# @app.get('/get-item/{item_id}')
# def get_item(item_id: int): # must match name. Has type hint
#     return inventory[item_id]

@app.get('/get-item/{item_id}') # if item_id isn't passed, it defaults to None
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view")): # must match name. Has type hint
    return inventory[item_id]

@app.get('/get-by-name') # it will assume name is a query parameter since it is not a path parameter
def get_item(name: Optional[str] = Query(None, title="Name", description="Name of item.", max_length=10, min_length=2)): # you can make it optional by giving it a default value. You can just use str instead of Optional[str]
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found.")

@app.post('/create-item/{item_id}') # for request body, you must use a type that inherits from base model
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item already exists." }
    
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item ID not found.")
        # return {"Error": "Item ID does not exist"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The Id of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item ID not found.")
        # return {"Error": "ID does not exists."}

    del inventory[item_id]
    return {"Success": "Item deleted!"}