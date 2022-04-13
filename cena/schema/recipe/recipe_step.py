from typing import Optional
from uuid import UUID, uuid4

from pydantic import UUID4, Field

from cena.schema._cena import CenaModel


class IngredientReferences(CenaModel):
    """
    A list of ingredient references.
    """

    reference_id: Optional[UUID4]

    class Config:
        orm_mode = True


class RecipeStep(CenaModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    title: Optional[str] = ""
    text: str
    ingredient_references: list[IngredientReferences] = []

    class Config:
        orm_mode = True
