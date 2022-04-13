from pydantic import UUID4

from cena.schema._cena import CenaModel

from .user import PrivateUser


class ForgotPassword(CenaModel):
    email: str


class ValidateResetToken(CenaModel):
    token: str


class ResetPassword(ValidateResetToken):
    email: str
    password: str
    passwordConfirm: str


class SavePasswordResetToken(CenaModel):
    user_id: UUID4
    token: str


class PrivatePasswordResetToken(SavePasswordResetToken):
    user: PrivateUser

    class Config:
        orm_mode = True
