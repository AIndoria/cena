from functools import cached_property

from sqlalchemy.orm import Session

from cena.db.models.group import Group, GroupMealPlan, ReportEntryModel, ReportModel
from cena.db.models.group.cookbook import CookBook
from cena.db.models.group.events import GroupEventNotifierModel
from cena.db.models.group.exports import GroupDataExportsModel
from cena.db.models.group.invite_tokens import GroupInviteToken
from cena.db.models.group.mealplan import GroupMealPlanRules
from cena.db.models.group.preferences import GroupPreferencesModel
from cena.db.models.group.shopping_list import (
    ShoppingList,
    ShoppingListItem,
    ShoppingListItemRecipeReference,
    ShoppingListRecipeReference,
)
from cena.db.models.group.webhooks import GroupWebhooksModel
from cena.db.models.labels import MultiPurposeLabel
from cena.db.models.recipe.category import Category
from cena.db.models.recipe.comment import RecipeComment
from cena.db.models.recipe.ingredient import IngredientFoodModel, IngredientUnitModel
from cena.db.models.recipe.recipe import RecipeModel
from cena.db.models.recipe.shared import RecipeShareTokenModel
from cena.db.models.recipe.tag import Tag
from cena.db.models.recipe.tool import Tool
from cena.db.models.server.task import ServerTaskModel
from cena.db.models.users import LongLiveToken, User
from cena.db.models.users.password_reset import PasswordResetModel
from cena.repos.repository_foods import RepositoryFood
from cena.repos.repository_meal_plan_rules import RepositoryMealPlanRules
from cena.repos.repository_units import RepositoryUnit
from cena.schema.cookbook.cookbook import ReadCookBook
from cena.schema.group.group_events import GroupEventNotifierOut
from cena.schema.group.group_exports import GroupDataExport
from cena.schema.group.group_preferences import ReadGroupPreferences
from cena.schema.group.group_shopping_list import (
    ShoppingListItemOut,
    ShoppingListItemRecipeRefOut,
    ShoppingListOut,
    ShoppingListRecipeRefOut,
)
from cena.schema.group.invite_token import ReadInviteToken
from cena.schema.group.webhook import ReadWebhook
from cena.schema.labels import MultiPurposeLabelOut
from cena.schema.meal_plan.new_meal import ReadPlanEntry
from cena.schema.meal_plan.plan_rules import PlanRulesOut
from cena.schema.recipe import Recipe, RecipeCommentOut, RecipeTool
from cena.schema.recipe.recipe_category import CategoryOut, TagOut
from cena.schema.recipe.recipe_ingredient import IngredientFood, IngredientUnit
from cena.schema.recipe.recipe_share_token import RecipeShareToken
from cena.schema.reports.reports import ReportEntryOut, ReportOut
from cena.schema.server import ServerTask
from cena.schema.user import GroupInDB, LongLiveTokenInDB, PrivateUser
from cena.schema.user.user_passwords import PrivatePasswordResetToken

from .repository_generic import RepositoryGeneric
from .repository_group import RepositoryGroup
from .repository_meals import RepositoryMeals
from .repository_recipes import RepositoryRecipes
from .repository_shopping_list import RepositoryShoppingList
from .repository_users import RepositoryUsers

PK_ID = "id"
PK_SLUG = "slug"
PK_TOKEN = "token"
PK_GROUP_ID = "group_id"


class RepositoryCategories(RepositoryGeneric[CategoryOut, Category]):
    def get_empty(self):
        return self.session.query(Category).filter(~Category.recipes.any()).all()


class RepositoryTags(RepositoryGeneric[TagOut, Tag]):
    def get_empty(self):
        return self.session.query(Tag).filter(~Tag.recipes.any()).all()


class AllRepositories:
    def __init__(self, session: Session) -> None:
        """
        `AllRepositories` class is the data access layer for all database actions within
        Cena. Database uses composition from classes derived from AccessModel. These
        can be substantiated from the AccessModel class or through inheritance when
        additional methods are required.
        """

        self.session = session

    # ================================================================
    # Recipe

    @cached_property
    def recipes(self) -> RepositoryRecipes:
        return RepositoryRecipes(self.session, PK_SLUG, RecipeModel, Recipe)

    @cached_property
    def ingredient_foods(self) -> RepositoryFood:
        return RepositoryFood(self.session, PK_ID, IngredientFoodModel, IngredientFood)

    @cached_property
    def ingredient_units(self) -> RepositoryUnit:
        return RepositoryUnit(self.session, PK_ID, IngredientUnitModel, IngredientUnit)

    @cached_property
    def tools(self) -> RepositoryGeneric[RecipeTool, Tool]:
        return RepositoryGeneric(self.session, PK_ID, Tool, RecipeTool)

    @cached_property
    def comments(self) -> RepositoryGeneric[RecipeCommentOut, RecipeComment]:
        return RepositoryGeneric(self.session, PK_ID, RecipeComment, RecipeCommentOut)

    @cached_property
    def categories(self) -> RepositoryCategories:
        return RepositoryCategories(self.session, PK_ID, Category, CategoryOut)

    @cached_property
    def tags(self) -> RepositoryTags:
        return RepositoryTags(self.session, PK_ID, Tag, TagOut)

    @cached_property
    def recipe_share_tokens(self) -> RepositoryGeneric[RecipeShareToken, RecipeShareTokenModel]:
        return RepositoryGeneric(self.session, PK_ID, RecipeShareTokenModel, RecipeShareToken)

    # ================================================================
    # User

    @cached_property
    def users(self) -> RepositoryUsers:
        return RepositoryUsers(self.session, PK_ID, User, PrivateUser)

    @cached_property
    def api_tokens(self) -> RepositoryGeneric[LongLiveTokenInDB, LongLiveToken]:
        return RepositoryGeneric(self.session, PK_ID, LongLiveToken, LongLiveTokenInDB)

    @cached_property
    def tokens_pw_reset(self) -> RepositoryGeneric[PrivatePasswordResetToken, PasswordResetModel]:
        return RepositoryGeneric(self.session, PK_TOKEN, PasswordResetModel, PrivatePasswordResetToken)

    # ================================================================
    # Group

    @cached_property
    def server_tasks(self) -> RepositoryGeneric[ServerTask, ServerTaskModel]:
        return RepositoryGeneric(self.session, PK_ID, ServerTaskModel, ServerTask)

    @cached_property
    def groups(self) -> RepositoryGroup:
        return RepositoryGroup(self.session, PK_ID, Group, GroupInDB)

    @cached_property
    def group_invite_tokens(self) -> RepositoryGeneric[ReadInviteToken, GroupInviteToken]:
        return RepositoryGeneric(self.session, PK_TOKEN, GroupInviteToken, ReadInviteToken)

    @cached_property
    def group_preferences(self) -> RepositoryGeneric[ReadGroupPreferences, GroupPreferencesModel]:
        return RepositoryGeneric(self.session, PK_GROUP_ID, GroupPreferencesModel, ReadGroupPreferences)

    @cached_property
    def group_exports(self) -> RepositoryGeneric[GroupDataExport, GroupDataExportsModel]:
        return RepositoryGeneric(self.session, PK_ID, GroupDataExportsModel, GroupDataExport)

    @cached_property
    def group_reports(self) -> RepositoryGeneric[ReportOut, ReportModel]:
        return RepositoryGeneric(self.session, PK_ID, ReportModel, ReportOut)

    @cached_property
    def group_report_entries(self) -> RepositoryGeneric[ReportEntryOut, ReportEntryModel]:
        return RepositoryGeneric(self.session, PK_ID, ReportEntryModel, ReportEntryOut)

    @cached_property
    def cookbooks(self) -> RepositoryGeneric[ReadCookBook, CookBook]:
        return RepositoryGeneric(self.session, PK_ID, CookBook, ReadCookBook)

    # ================================================================
    # Meal Plan

    @cached_property
    def meals(self) -> RepositoryMeals:
        return RepositoryMeals(self.session, PK_ID, GroupMealPlan, ReadPlanEntry)

    @cached_property
    def group_meal_plan_rules(self) -> RepositoryMealPlanRules:
        return RepositoryMealPlanRules(self.session, PK_ID, GroupMealPlanRules, PlanRulesOut)

    @cached_property
    def webhooks(self) -> RepositoryGeneric[ReadWebhook, GroupWebhooksModel]:
        return RepositoryGeneric(self.session, PK_ID, GroupWebhooksModel, ReadWebhook)

    # ================================================================
    # Shopping List

    @cached_property
    def group_shopping_lists(self) -> RepositoryShoppingList:
        return RepositoryShoppingList(self.session, PK_ID, ShoppingList, ShoppingListOut)

    @cached_property
    def group_shopping_list_item(self) -> RepositoryGeneric[ShoppingListItemOut, ShoppingListItem]:
        return RepositoryGeneric(self.session, PK_ID, ShoppingListItem, ShoppingListItemOut)

    @cached_property
    def group_shopping_list_item_references(
        self,
    ) -> RepositoryGeneric[ShoppingListItemRecipeRefOut, ShoppingListItemRecipeReference]:
        return RepositoryGeneric(self.session, PK_ID, ShoppingListItemRecipeReference, ShoppingListItemRecipeRefOut)

    @cached_property
    def group_shopping_list_recipe_refs(
        self,
    ) -> RepositoryGeneric[ShoppingListRecipeRefOut, ShoppingListRecipeReference]:
        return RepositoryGeneric(self.session, PK_ID, ShoppingListRecipeReference, ShoppingListRecipeRefOut)

    @cached_property
    def group_multi_purpose_labels(self) -> RepositoryGeneric[MultiPurposeLabelOut, MultiPurposeLabel]:
        return RepositoryGeneric(self.session, PK_ID, MultiPurposeLabel, MultiPurposeLabelOut)

    # ================================================================
    # Group Events

    @cached_property
    def group_event_notifier(self) -> RepositoryGeneric[GroupEventNotifierOut, GroupEventNotifierModel]:
        return RepositoryGeneric(self.session, PK_ID, GroupEventNotifierModel, GroupEventNotifierOut)
