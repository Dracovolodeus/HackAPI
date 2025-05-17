from pydantic import BaseModel


class InviteURLCreate(BaseModel):
    team_id: int


class InviteURLRead(BaseModel):
    url: str
