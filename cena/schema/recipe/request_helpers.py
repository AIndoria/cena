from pydantic import BaseModel

from cena.schema._cena import CenaModel

# TODO: Should these exist?!?!?!?!?


class RecipeSlug(CenaModel):
    slug: str


class SlugResponse(BaseModel):
    class Config:
        schema_extra = {"example": "adult-mac-and-cheese"}
