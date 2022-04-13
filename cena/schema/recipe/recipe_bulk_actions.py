import enum

from cena.schema._cena import CenaModel
from cena.schema.recipe.recipe_category import CategoryBase, TagBase


class ExportTypes(str, enum.Enum):
    JSON = "json"


class ExportBase(CenaModel):
    recipes: list[str]


class ExportRecipes(ExportBase):
    export_type: ExportTypes = ExportTypes.JSON


class AssignCategories(ExportBase):
    categories: list[CategoryBase]


class AssignTags(ExportBase):
    tags: list[TagBase]


class DeleteRecipes(ExportBase):
    pass


class BulkActionError(CenaModel):
    recipe: str
    error: str


class BulkActionsResponse(CenaModel):
    success: bool
    message: str
    errors: list[BulkActionError] = []
