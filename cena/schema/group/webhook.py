from uuid import UUID

from pydantic import UUID4

from cena.schema._cena import CenaModel


class CreateWebhook(CenaModel):
    enabled: bool = True
    name: str = ""
    url: str = ""
    time: str = "00:00"


class SaveWebhook(CreateWebhook):
    group_id: UUID


class ReadWebhook(SaveWebhook):
    id: UUID4

    class Config:
        orm_mode = True
