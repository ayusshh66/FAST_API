import string

from fastapi import FastAPI, Query, HTTPException
from model import MenuItems, MenuResponse
from data import menu_item
import uvicorn

app = FastAPI(
    title="chai point menu api",
    description="read only menu api"
)

@app.get("/")
def root():
    return {
        "message": "the server is up and running"
    }

@app.get("/menu", response_model=MenuResponse)
def get_menu(category:str| None = Query(None, description="Filtered by chai, snack or combo")):
    if category:
        filtered = [items for items in menu_item if items["category"] == category.lower() ]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"no item found in category: {category}")
        return MenuResponse(count=len(filtered), items=[MenuItems(**item) for item in filtered])
    return MenuResponse(count=len(menu_item), items= [MenuItems(**item) for item in menu_item])

@app.get("/menu/{item_id}", response_model=MenuItems)
def get_item(item_id:int):
    for item in menu_item:
        if item["id"] == item_id:
            return item;
        raise HTTPException(status_code = 404, detail = f"no item found with {item_id}")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
