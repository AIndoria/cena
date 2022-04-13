from typing import Optional

from cena.schema._cena import CenaModel


class RecipeAsset(CenaModel):
    name: str
    icon: str
    file_name: Optional[str]

    class Config:
        orm_mode = True
