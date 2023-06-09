from typing import Union
from databases.interfaces import Record


from databases import Database
import sqlalchemy


class DatabaseOperations:
    def __init__(self, database_url):
        metadata = sqlalchemy.MetaData()

        self.database = Database(database_url)
        self.questions = sqlalchemy.Table(
            "polls_question",
            metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("question_text", sqlalchemy.String),
            sqlalchemy.Column("pub_date", sqlalchemy.DateTime),
        )

    async def read_questions(self):
        query = self.questions.select()
        return await self.database.fetch_all(query)

    async def read_question(self, question_id: int) -> Union[Record, None]:
        query = self.questions.select().where(self.questions.c.id == question_id)
        return await self.database.fetch_one(query)
