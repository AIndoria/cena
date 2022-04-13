from pydantic import UUID4
from pydantic.utils import GetterDict

from cena.schema._cena import CenaModel


class CategoryIn(CenaModel):
    name: str


class CategorySave(CategoryIn):
    group_id: UUID4


class CategoryBase(CategoryIn):
    id: UUID4
    slug: str

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(_cls, name_orm):
            return {
                **GetterDict(name_orm),
            }


class CategoryOut(CategoryBase):
    slug: str

    class Config:
        orm_mode = True


class RecipeCategoryResponse(CategoryBase):
    recipes: "list[RecipeSummary]" = []

    class Config:
        orm_mode = True


class TagIn(CategoryIn):
    pass


class TagSave(TagIn):
    group_id: UUID4


class TagBase(CategoryBase):
    pass


class TagOut(TagSave):
    id: UUID4
    slug: str

    class Config:
        orm_mode = True


class RecipeTagResponse(RecipeCategoryResponse):
    pass


from cena.schema.recipe.recipe import RecipeSummary

RecipeCategoryResponse.update_forward_refs()
RecipeTagResponse.update_forward_refs()
