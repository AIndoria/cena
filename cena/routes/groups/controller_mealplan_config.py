from cena.routes._base.base_controllers import BaseUserController
from cena.routes._base.controller import controller
from cena.routes._base.mixins import HttpRepo
from cena.routes._base.routers import UserAPIRouter
from cena.schema.recipe.recipe_category import CategoryBase
from cena.schema.user.user import GroupInDB

router = UserAPIRouter(prefix="/groups/categories", tags=["Groups: Mealplan Categories"])


@controller(router)
class GroupMealplanConfigController(BaseUserController):
    @property
    def mixins(self):
        return HttpRepo[GroupInDB, GroupInDB, GroupInDB](self.repos.groups, self.deps.logger)

    @router.get("", response_model=list[CategoryBase])
    def get_mealplan_categories(self):
        data = self.mixins.get_one(self.deps.acting_user.group_id)
        return data.categories

    @router.put("", response_model=list[CategoryBase])
    def update_mealplan_categories(self, new_categories: list[CategoryBase]):
        data = self.mixins.get_one(self.deps.acting_user.group_id)
        data.categories = new_categories
        return self.mixins.update_one(data, data.id).categories
