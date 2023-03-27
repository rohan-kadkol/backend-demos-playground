from typing import Optional, Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from databases import Database
import sqlalchemy

import time
from helpers.database_operations import DatabaseOperations

from models.models import Question

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

DATABASE_URL = "sqlite:///../django/db.sqlite3"
databaseOperations = DatabaseOperations(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await databaseOperations.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await databaseOperations.database.disconnect()


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


@app.get("/questions/")
async def read_questions():
    return await databaseOperations.read_questions()


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
            "content": {"application/json": {"example": {"message": "Item not found"}}},
        }
    },
)
async def read_question(question_id: int):
    response = await databaseOperations.read_question(question_id)
    if response is None:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return response


@app.get("/frontend/questions/", response_class=HTMLResponse)
async def frontendQuestions(request: Request):
    print("HERE")
    questions = await databaseOperations.read_questions()
    return templates.TemplateResponse(
        "index.html", {"request": request, "questions": questions}
    )


@app.get("/frontend/questions/{question_id}", response_class=HTMLResponse)
async def frontendQuestion(request: Request, question_id: int):
    question = await databaseOperations.read_question(question_id)
    return templates.TemplateResponse(
        "details.html", {"request": request, "question": question}
    )
