from typing import List
from injector import inject
from pymongo.results import InsertOneResult
from pymongo import ReturnDocument
from bson import ObjectId
from app.channels.schemas import CreateChannelResponse, ChannelModel, ChannelUpdateModel
from pymongo.asynchronous.database import AsyncDatabase, AsyncCollection


@inject
class ChannelRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.collection: AsyncCollection = db.get_collection("channels")

    async def create_channel(self, channel: ChannelModel) -> CreateChannelResponse:
        response: InsertOneResult = await self.collection.insert_one(channel.model_dump())
        return CreateChannelResponse(id=response.inserted_id)

    async def get_channel(self, channel_id: str, tenant_id: str) -> ChannelModel | None:
        return await self.collection.find_one(
            {"_id": ObjectId(channel_id), "tenant_id": tenant_id}
        )

    async def update_channel(
        self, channel_id: str, channel: ChannelUpdateModel, tenant_id: str
    ) -> ChannelModel | None:
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(channel_id), "tenant_id": tenant_id},
            {"$set": {**channel.model_dump()}},
            return_document=ReturnDocument.AFTER,
        )

    def get_channels(self) -> List[None]:
        pass

    def delete_channel(self, channel) -> None:
        pass
