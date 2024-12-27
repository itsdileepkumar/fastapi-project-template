from injector import inject
from pymongo.asynchronous.database import AsyncDatabase, AsyncCollection
from app.teams.schemas import TeamModel, CreateTeamResponse
from pymongo.results import InsertOneResult


@inject
class TeamsRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self.collection: AsyncCollection = db.get_collection("teams")


    async def create_team(self, team: TeamModel) -> CreateTeamResponse:
        response: InsertOneResult = await self.collection.insert_one(team.model_dump())
        return CreateTeamResponse(id=response.inserted_id)
        
