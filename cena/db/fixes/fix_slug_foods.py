import json

from cena.core import root_logger
from cena.repos.repository_factory import AllRepositories
from cena.repos.seed.resources import foods as food_resources


def fix_slug_food_names(db: AllRepositories):
    check_for_food = "dairy-products-and-dairy-substitutes"

    food = db.ingredient_foods.get_one(check_for_food, "name")

    logger = root_logger.get_logger("init_db")

    if not food:
        logger.info("No food found with slug: '{}' skipping fix".format(check_for_food))
        return

    all_foods = db.ingredient_foods.get_all()

    seed_foods: dict[str, str] = json.loads(food_resources.en_US.read_text())

    for food in all_foods:
        if food.name in seed_foods:
            food.name = seed_foods[food.name]
            logger.info("Updating food: {}".format(food.name))
            db.ingredient_foods.update(food.id, food)
