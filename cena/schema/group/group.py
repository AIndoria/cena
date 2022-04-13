from pydantic import UUID4

from cena.schema._cena import CenaModel

from .group_preferences import UpdateGroupPreferences


class GroupAdminUpdate(CenaModel):
    id: UUID4
    name: str
    preferences: UpdateGroupPreferences
