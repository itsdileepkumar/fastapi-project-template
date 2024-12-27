from injector import (
    Module,
    Binder,
    singleton,
    Injector,
    ClassProvider,
    InstanceProvider,
)
from app.channels.module import ChannelModule
from app.teams.module import TeamsModule
from app.core.security import Security
from app.config import settings
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Security, to=ClassProvider(Security), scope=singleton)
        binder.bind(
            AsyncDatabase,
            to=InstanceProvider(
                AsyncMongoClient(settings.MONGO_URL, uuidRepresentation="standard")[
                    settings.DATABASE_NAME
                ]
            ),
        )
        # binder.install(ChannelModule)
        binder.install(TeamsModule)
        print("AppModule initialized")


injector = Injector([AppModule])
