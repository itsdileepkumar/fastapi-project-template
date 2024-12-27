from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, BeforeValidator, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]
ContextList = Annotated[
    List[Dict[str, str]],
    BeforeValidator(lambda x: [{"key": k, "value": v} for k, v in x.items()]),
]
ContextListBack = Annotated[
    Dict[str, str],
    BeforeValidator(lambda x: {item["key"]: item["value"] for item in x}),
]


class ChannelStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    CLOSED = "closed"


class Resolution(BaseModel):
    type: Optional[str] = None
    comment: Optional[str] = None
    actor: Optional[UUID] = None
    ts: Optional[datetime] = None


class Channel(BaseModel):
    name: str
    desc: Optional[str] = None
    app_id: str
    context: Optional[Dict[str, str]] = Field(default_factory=dict)
    members: Optional[List[UUID]] = Field(default_factory=dict)


class CreateChannelResponse(BaseModel):
    id: PyObjectId


class GetChannelResponse(Channel, CreateChannelResponse):
    context: Optional[ContextListBack] = Field(default_factory=list)
    owner: UUID
    status: ChannelStatus
    resolution: Optional[Resolution] = None
    exp_at: Optional[datetime] = None
    crt_at: Optional[datetime]
    upd_at: Optional[datetime]


class GetChannelsListReponse(BaseModel):
    entities: List[GetChannelResponse]


class UpdateChannelResponse(GetChannelResponse):
    pass


class ChannelModel(BaseModel):
    name: str
    desc: Optional[str] = None
    app_id: str
    context: Optional[ContextList] = Field(default_factory=list)
    members: Optional[List[UUID]] = Field(default_factory=list)
    owner: str
    status: ChannelStatus
    resolution: Optional[Resolution] = None
    tenant_id: str
    exp_at: Optional[datetime] = None
    crt_at: Optional[datetime] = Field(default_factory=datetime.now)
    upd_at: Optional[datetime] = Field(default_factory=datetime.now)

class ChannelUpdateModel(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    app_id: Optional[str] = None
    context: Optional[ContextList] = Field(default_factory=list)
    members: Optional[List[UUID]] = Field(default_factory=list)
    upd_at: Optional[datetime] = Field(default_factory=datetime.now)
