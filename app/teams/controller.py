from fastapi import APIRouter, Request
from app.app_module import injector
from app.teams.service import TeamsService
from app.teams.schemas import Team, CreateTeamResponse

team_service: TeamsService = injector.get(TeamsService)


class TeamsController:
    print("TeamsController initialized")
    router = APIRouter()

    @router.post("", response_model=CreateTeamResponse)
    async def create_team(team: Team, request: Request) -> CreateTeamResponse:
        user_id: str = request.state.__getattr__("sub")
        tenant_id: str = request.state.__getattr__("by_realm_id")
        return await team_service.create_team(team, user_id, tenant_id)
