import typing

from pydantic import UUID4

from cena.schema._cena import CenaModel


class RecipeToolCreate(CenaModel):
    name: str
    on_hand: bool = False


class RecipeToolSave(RecipeToolCreate):
    group_id: UUID4


class RecipeTool(RecipeToolCreate):
    id: UUID4
    slug: str

    class Config:
        orm_mode = True


class RecipeToolResponse(RecipeTool):
    recipes: typing.List["Recipe"] = []

    class Config:
        orm_mode = True


from .recipe import Recipe

RecipeToolResponse.update_forward_refs()
