from injector import Module, Binder, singleton, ClassProvider
from app.channels.repository import ChannelRepository
from app.channels.service import ChannelService


class ChannelModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ChannelRepository, to=ClassProvider(ChannelRepository), scope=singleton)
        print("ChannelRepository initialized")
        binder.bind(ChannelService, to=ClassProvider(ChannelService), scope=singleton)
        print("ChannelService initialized")
        print("ChannelModule initialized")
