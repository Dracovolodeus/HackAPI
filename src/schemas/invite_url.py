from pydantic import BaseModel, field_validator
import datetime


class InviteURLBase(BaseModel):
    url: str


class InviteURLCreate(InviteURLBase):
    creator_id: int

    @field_validator("url", mode="before")
    def gen_url(cls, v):
        now = datetime.datetime.now()
        return f"{v}"


class InviteURLRead(InviteURLBase):
    ...
