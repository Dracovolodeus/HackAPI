from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    idea: str
    idea_detail: str
    leader_id: int
    hackathon_id: int


class TeamCreate(TeamBase): ...


class TeamCreateForAPI(BaseModel):
    name: str
    idea: str
    idea_detail: str
    hackathon_id: int

class TeamRead(TeamBase): ...
