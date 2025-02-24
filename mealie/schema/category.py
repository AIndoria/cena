from typing import List, Optional

from fastapi_camelcase import CamelModel
from cena.schema.recipe import Recipe
from pydantic.utils import GetterDict


class CategoryIn(CamelModel):
    name: str


class CategoryBase(CategoryIn):
    id: int
    slug: str

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(_cls, name_orm):
            return {
                **GetterDict(name_orm),
                "total_recipes": len(name_orm.recipes),
            }


class RecipeCategoryResponse(CategoryBase):
    recipes: Optional[List[Recipe]]

    class Config:
        schema_extra = {"example": {"id": 1, "name": "dinner", "recipes": [{}]}}


class TagIn(CategoryIn):
    pass


class TagBase(CategoryBase):
    pass


class RecipeTagResponse(RecipeCategoryResponse):
    pass
