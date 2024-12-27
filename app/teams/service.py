from uuid import UUID
from injector import inject
from app.teams.repository import TeamsRepository
from app.teams.schemas import Team, TeamModel, CreateTeamResponse


@inject
class TeamsService:
    def __init__(self, team_repository: TeamsRepository):
        self.team_repository: TeamsRepository = team_repository

    async def create_team(
        self, team: Team, user_id: str, tenant_id: str
    ) -> CreateTeamResponse:
        new_team: TeamModel = TeamModel(
            name=team.name,
            desc=team.desc,
            members=[UUID(id) for id in team.members],
            owners=[UUID(user_id)],
            tenant_id=UUID(tenant_id),
            crtd_by=UUID(user_id),
            updt_by=UUID(user_id),
        )

        return await self.team_repository.create_team(new_team)

    async def get_team(self, team_id: str, tenant_id: str):
        pass

    async def update_team(self, team_id: int, team: Team, tenant_id: str):
        pass

    async def delete_team(self, team_id: int, tenant_id: str):
        pass
