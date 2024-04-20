import json
from typing import Any

from beanie import init_beanie, PydanticObjectId  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict
from models.feedback_model import DbFeedback
from models.note_model import DbNote
from models.user_model import DbUser
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pydantic import BaseModel, Field


class Settings(BaseSettings):
    DB_USER: str = Field(default="")
    DB_PASS: str = Field(default="")
    SECRET_KEY: str = Field(default="")

    model_config = SettingsConfigDict(env_file=".env")

    async def initialize_database(self):
        DATABASE_URL: str = f"mongodb+srv://{self.DB_USER}:{self.DB_PASS}@scribedb.klymspw.mongodb.net/"
        client = AsyncIOMotorClient(DATABASE_URL)
        await init_beanie(
            database=client.ScribeDB,
            document_models=[DbFeedback, DbNote, DbUser]
        )


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> PydanticObjectId:
        m = await document.create()
        return m.id

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> list[Any]:
        docs = await self.model.find_all().to_list()
        return docs
    
    async def get_by_field(self, field: str, value: Any) -> list:
        docs = await self.model.find({field: value}).to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.model_dump_json(exclude_defaults=True)
        des_body = json.loads(des_body)
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.set(des_body)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
