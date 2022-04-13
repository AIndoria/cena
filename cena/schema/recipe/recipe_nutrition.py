from typing import Optional

from cena.schema._cena import CenaModel


class Nutrition(CenaModel):
    calories: Optional[str]
    fat_content: Optional[str]
    protein_content: Optional[str]
    carbohydrate_content: Optional[str]
    fiber_content: Optional[str]
    sodium_content: Optional[str]
    sugar_content: Optional[str]

    class Config:
        orm_mode = True
