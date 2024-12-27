from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, BeforeValidator, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

# Team DB Model
class TeamModel(BaseModel):
    name: str
    desc: Optional[str]
    tags: Optional[List[str]] = Field(default_factory=list)
    members: Optional[List[UUID]] = Field(default_factory=list)
    owners: Optional[List[UUID]] = Field(default_factory=list)
    channels: Optional[List[UUID]] = Field(default_factory=list)
    props: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    tenant_id: UUID
    crtd_by: UUID
    updt_by: UUID
    crtd_at: Optional[datetime] = Field(default_factory=datetime.now)
    uptd_at: Optional[datetime] = Field(default_factory=datetime.now)

# Team Request Schema
class Team(BaseModel):
    name: str
    desc: Optional[str]
    tags: Optional[List[str]] = Field(default_factory=list)
    members: Optional[List[str]] = Field(default_factory=list)
    channels: Optional[List[str]] = Field(default_factory=list)
    props: Optional[Dict[str, str]] = Field(default_factory=dict)

# Create Team Response Schema
class CreateTeamResponse(BaseModel):
    id: PyObjectId

# Get Team Response Schema
class GetTeamResponse(Team, CreateTeamResponse):
    crt_at: datetime
    upd_at: datetime

# Update Team Response Schema
class UpdateTeamResponse(GetTeamResponse):
    pass

# Add Members Request Schema
class AddMemberRequest(BaseModel):
    member: List[str]

