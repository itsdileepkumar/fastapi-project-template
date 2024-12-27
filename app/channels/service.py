from typing import List
from injector import inject
from fastapi.exceptions import HTTPException
from app.channels.repository import ChannelRepository
from app.channels.schemas import (
    CreateChannelResponse,
    GetChannelResponse,
    Channel,
    ChannelModel,
    ChannelStatus,
    ChannelUpdateModel
)


@inject
class ChannelService:
    def __init__(self, channel_repository: ChannelRepository):
        self.channel_repository = channel_repository

    async def create_channel(
        self, channel: Channel, user_id: str, tenant_id: str
    ) -> CreateChannelResponse:
        new_channel: ChannelModel = ChannelModel(
            name=channel.name,
            description=channel.desc,
            app_id=channel.app_id,
            context=channel.context,
            members=channel.members,
            owner=user_id,
            status=ChannelStatus.ACTIVE,
            resolution=None,
            tenant_id=tenant_id,
        )
        return await self.channel_repository.create_channel(new_channel)

    async def get_channel(self, channel_id: str, tenant_id: str) -> GetChannelResponse:
        response: ChannelModel | None = await self.channel_repository.get_channel(
            channel_id, tenant_id
        )
        if response is None:
            raise HTTPException(
                status_code=404, detail=f"Channel with id {channel_id} not found"
            )
        return GetChannelResponse(id=response["_id"], **response)

    async def update_channel(self, channel_id: int, channel: Channel, tenant_id: str) -> None:
        updated_channel: ChannelUpdateModel = ChannelUpdateModel(
            name=channel.name,
            description=channel.desc,
            app_id=channel.app_id,
            context=channel.context,
            members=channel.members,
        )
        response: ChannelModel | None = await self.channel_repository.update_channel(
            channel_id, updated_channel, tenant_id
        )
        if response is None:
            raise HTTPException(
                status_code=404, detail=f"Channel with id {channel_id} not found"
            )
        return GetChannelResponse(id=response["_id"], **response)

    def get_all_channels(self) -> List[None]:
        pass

    def delete_channel(self, channel_id: int) -> None:
        pass
