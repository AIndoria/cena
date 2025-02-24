from fastapi import Depends
from cena.core.root_logger import get_logger
from cena.db.database import db
from cena.db.db_setup import generate_session
from cena.routes.deps import get_current_user
from cena.routes.routers import UserAPIRouter
from cena.schema.meal import MealPlanOut
from cena.schema.recipe import Recipe
from cena.schema.shopping_list import ListItem, ShoppingListIn, ShoppingListOut
from cena.schema.user import UserInDB
from sqlalchemy.orm.session import Session

logger = get_logger()

router = UserAPIRouter(prefix="/api/meal-plans", tags=["Meal Plan"])


@router.get("/{id}/shopping-list")
def get_shopping_list(
    id: str,
    session: Session = Depends(generate_session),
    current_user: UserInDB = Depends(get_current_user),
):

    mealplan: MealPlanOut = db.meals.get(session, id)

    all_ingredients = []

    for plan_day in mealplan.plan_days:
        for meal in plan_day.meals:
            if not meal.slug:
                continue

            try:
                recipe: Recipe = db.recipes.get(session, meal.slug)
                all_ingredients += recipe.recipe_ingredient
            except Exception:
                logger.error("Recipe Not Found")

    new_list = ShoppingListIn(
        name="MealPlan Shopping List", group=current_user.group, items=[ListItem(text=t.note) for t in all_ingredients]
    )

    created_list: ShoppingListOut = db.shopping_lists.create(session, new_list)

    mealplan.shopping_list = created_list.id

    db.meals.update(session, mealplan.uid, mealplan)

    return created_list
