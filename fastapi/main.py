from typing import Optional, Union

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import time

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


async def fake_video_streamer():
    for i in range(10):
        time.sleep(0.5)
        yield b"some fake video bytes"


@app.get("/video")
async def fake_video_streamer_endpoint():
    return StreamingResponse(fake_video_streamer())
