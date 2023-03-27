from typing import Optional, Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from databases import Database
import sqlalchemy

import time

from models.models import Question

app = FastAPI()
DATABASE_URL = "sqlite:///../django/db.sqlite3"
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

questions = sqlalchemy.Table(
    "polls_question",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("question_text", sqlalchemy.String),
    sqlalchemy.Column("pub_date", sqlalchemy.DateTime),
)


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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


@app.get("/questions/", response_model=list[Question])
async def read_questions():
    query = questions.select()
    return await database.fetch_all(query)


@app.get(
    "/questions/{question_id}",
    response_model=Question,
    responses={
        404: {
            "description": "When the question with the given question_id is not found",
            # "content": {
            #     "application/json": {
            #         "example": {"id": "bar", "value": "The bar tenders"}
            #     }
            # },
            "content": {
                "application/json": {
                    "example": {"message": "Item not found"}
                }
            },
        }
    },
)
async def read_question(question_id: int):
    query = questions.select().where(questions.c.id == question_id)
    response = await database.fetch_one(query)
    print(response)
    if response is None:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return response
