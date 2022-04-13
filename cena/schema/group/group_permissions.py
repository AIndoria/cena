from pydantic import UUID4

from cena.schema._cena import CenaModel


class SetPermissions(CenaModel):
    user_id: UUID4
    can_manage: bool = False
    can_invite: bool = False
    can_organize: bool = False
