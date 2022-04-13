from cena.schema._cena import CenaModel


class GetAll(CenaModel):
    start: int = 0
    limit: int = 999
