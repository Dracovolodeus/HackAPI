from pydantic import BaseModel


class HackathonBase(BaseModel):
    creator_user_id: int
    organization_name: str
    contacts: str
    description: str
    plan: str
    hackathon_name: str
    old_limitation: int
    email_text: str

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
    plan: str
    hackathon_name: str
    old_limitation: int
    email_text: str

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
