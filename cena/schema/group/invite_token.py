from uuid import UUID

from pydantic import NoneStr

from cena.schema._cena import CenaModel


class CreateInviteToken(CenaModel):
    uses: int


class SaveInviteToken(CenaModel):
    uses_left: int
    group_id: UUID
    token: str


class ReadInviteToken(CenaModel):
    token: str
    uses_left: int
    group_id: UUID

    class Config:
        orm_mode = True


class EmailInvitation(CenaModel):
    email: str
    token: str


class EmailInitationResponse(CenaModel):
    success: bool
    error: NoneStr = None
