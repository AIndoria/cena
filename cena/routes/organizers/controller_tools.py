from functools import cached_property

from fastapi import APIRouter, Depends
from pydantic import UUID4

from cena.routes._base.base_controllers import BaseUserController
from cena.routes._base.controller import controller
from cena.routes._base.mixins import HttpRepo
from cena.schema import mapper
from cena.schema.query import GetAll
from cena.schema.recipe.recipe import RecipeTool
from cena.schema.recipe.recipe_tool import RecipeToolCreate, RecipeToolResponse, RecipeToolSave

router = APIRouter(prefix="/tools", tags=["Organizer: Tools"])


@controller(router)
class RecipeToolController(BaseUserController):
    @cached_property
    def repo(self):
        return self.repos.tools.by_group(self.group_id)

    @property
    def mixins(self) -> HttpRepo:
        return HttpRepo[RecipeToolCreate, RecipeTool, RecipeToolCreate](self.repo, self.deps.logger)

    @router.get("", response_model=list[RecipeTool])
    def get_all(self, q: GetAll = Depends(GetAll)):
        return self.repo.get_all(start=q.start, limit=q.limit, override_schema=RecipeTool)

    @router.post("", response_model=RecipeTool, status_code=201)
    def create_one(self, data: RecipeToolCreate):
        save_data = mapper.cast(data, RecipeToolSave, group_id=self.group_id)
        return self.mixins.create_one(save_data)

    @router.get("/{item_id}", response_model=RecipeTool)
    def get_one(self, item_id: UUID4):
        return self.mixins.get_one(item_id)

    @router.put("/{item_id}", response_model=RecipeTool)
    def update_one(self, item_id: UUID4, data: RecipeToolCreate):
        return self.mixins.update_one(data, item_id)

    @router.delete("/{item_id}", response_model=RecipeTool)
    def delete_one(self, item_id: UUID4):
        return self.mixins.delete_one(item_id)  # type: ignore

    @router.get("/slug/{tool_slug}", response_model=RecipeToolResponse)
    async def get_one_by_slug(self, tool_slug: str):
        return self.repo.get_one(tool_slug, "slug", override_schema=RecipeToolResponse)
