import datetime
from pydantic import BaseModel


class Question(BaseModel):
    question_text: str
    pub_date: datetime.datetime

    def __str__(self) -> str:
        return f'Question: ("{self.question_text}", {self.pub_date})'

    def was_recently_published(self):
        threshold = datetime.datetime.now() - datetime.timedelta(days=1)
        return self.pub_date >= threshold


class Choice(BaseModel):
    id: int
    choice_text: str
    votes: int
    question_id: int
