from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from app.app_module import injector
from app.core.exception_handler import unified_exception_handler
from app.teams.controller import TeamsController
from app.channels.controller import ChannelController
from app.core.middlewares import auth_middleware
from pymongo.asynchronous.database import AsyncDatabase
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    db: AsyncDatabase = injector.get(AsyncDatabase)
    logging.info("Connecting to the database")
    await db.client.admin.command("ping")
    for route in app.routes:
        for method in route.methods:
            logging.info(f"Route - {method} - {route.path}")
    yield
    # Disconnect from the database
    logging.info("Disconnecting from the database")
    await db.client.close()


api_router = APIRouter(prefix="/api/v1", dependencies=[Depends(auth_middleware)])
api_router.include_router(TeamsController.router, prefix="/teams", tags=["teams"])
# api_router.include_router(
#     MemberController.router, prefix="/teams/{team_id}/members", tags=["members"]
# )
api_router.include_router(
    ChannelController.router, prefix="/teams/{team_id}/channels", tags=["channels"]
)
# api_router.include_router(
#     ChannelMembersController.router,
#     prefix="/teams/{team_id}/channels/{channel_id}/members",
#     tags=["channelMembers"],
# )
# api_router.include_router(
#     MessagesController.router,
#     prefix="/teams/{team_id}/channels/{channel_id}/messages",
#     tags=["messages"],
# )


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.add_exception_handler(Exception, unified_exception_handler)
