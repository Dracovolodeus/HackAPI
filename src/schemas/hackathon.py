from typing import Optional

from pydantic import BaseModel


class HackathonBase(BaseModel):
    creator_user_id: int
    organization_name: str
    contacts: str
    description: str
    hackathon_name: str
    city: str
    address: str
    is_offline: bool
    image_id: Optional[int] = None
    detail: list[dict[str, str]]

    reg_start_date: str
    reg_end_date: str
    reg_limitation: int

    start_date: str
    end_date: str


class HackathonCreate(HackathonBase): ...


class HackathonCreateForAPI(BaseModel):
    organization_name: str
    contacts: str
    description: str
    detail: list[dict[str, str]]
    hackathon_name: str
    city: str
    address: str
    is_offline: bool
    image_id: Optional[int]

    reg_start_date: str
    reg_end_date: str
    reg_limitation: int

    start_date: str
    end_date: str


class HackathonRead(HackathonBase):
    id: int
    admins_ids: list[int]
    jury_ids: list[int]
    teams_ids: list[int]
