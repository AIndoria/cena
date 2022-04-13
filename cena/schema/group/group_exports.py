from datetime import datetime

from pydantic import UUID4

from cena.schema._cena import CenaModel


class GroupDataExport(CenaModel):
    id: UUID4
    group_id: UUID4
    name: str
    filename: str
    path: str
    size: str
    expires: datetime

    class Config:
        orm_mode = True
