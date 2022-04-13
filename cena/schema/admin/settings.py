from typing import Optional

from pydantic import validator
from slugify import slugify

from cena.schema._cena import CenaModel

from ..recipe.recipe_category import RecipeCategoryResponse


class CustomPageBase(CenaModel):
    name: str
    slug: Optional[str]
    position: int
    categories: list[RecipeCategoryResponse] = []

    class Config:
        orm_mode = True

    @validator("slug", always=True, pre=True)
    def validate_slug(slug: str, values):
        name: str = values["name"]
        calc_slug: str = slugify(name)

        if slug != calc_slug:
            slug = calc_slug

        return slug


class CustomPageOut(CustomPageBase):
    id: int

    class Config:
        orm_mode = True
