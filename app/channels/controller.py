from fastapi import APIRouter, Depends, Request
from app.channels.schemas import CreateChannelResponse, Channel, GetChannelResponse
from app.channels.service import ChannelService
from app.app_module import injector


channel_service: ChannelService = injector.get(ChannelService)


class ChannelController:
    print("ChannelController initialized")

    router = APIRouter()

    @router.post("", response_model=CreateChannelResponse)
    async def create_channel(
        channel: Channel, request: Request
    ) -> CreateChannelResponse:
        user_id: str = request.state.__getattr__("sub")
        tenant_id: str = request.state.__getattr__("by_realm_id")
        return await channel_service.create_channel(channel, user_id, tenant_id)

    @router.get("/{channel_id}", response_model=GetChannelResponse)
    async def get_channel(channel_id: str, request: Request) -> GetChannelResponse:
        tenant_id: str = request.state.__getattr__("by_realm_id")
        return await channel_service.get_channel(channel_id, tenant_id)

    @router.put("/{channel_id}", response_model=GetChannelResponse)
    async def update_channel(
        channel_id: str, channel: Channel, request: Request
    ) -> GetChannelResponse:
        tenant_id: str = request.state.__getattr__("by_realm_id")
        return await channel_service.update_channel(channel_id, channel, tenant_id)
    
    @router.delete("/{channel_id}")
    async def delete_channel(channel_id: str, request: Request):
        pass