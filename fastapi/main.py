from typing import Optional, Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/{item_id}")
def add_item(item_id: int, q: Optional[str] = None):
    return f"Item with id{item_id} is added 😊"