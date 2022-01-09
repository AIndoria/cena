from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, orm

from mealie.db.models._model_base import BaseMixins, SqlAlchemyBase
from mealie.db.models.labels import MultiPurposeLabel

from .._model_utils import auto_init
from .._model_utils.guid import GUID


class IngredientUnitModel(SqlAlchemyBase, BaseMixins):
    __tablename__ = "ingredient_units"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    abbreviation = Column(String)
    fraction = Column(Boolean)
    ingredients = orm.relationship("RecipeIngredient", back_populates="unit")

    @auto_init()
    def __init__(self, **_) -> None:
        pass


class IngredientFoodModel(SqlAlchemyBase, BaseMixins):
    __tablename__ = "ingredient_foods"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    ingredients = orm.relationship("RecipeIngredient", back_populates="food")

    label_id = Column(GUID, ForeignKey("multi_purpose_labels.id"))
    label = orm.relationship(MultiPurposeLabel, uselist=False, back_populates="foods")

    @auto_init()
    def __init__(self, **_) -> None:
        pass


class RecipeIngredient(SqlAlchemyBase, BaseMixins):
    __tablename__ = "recipes_ingredients"
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    parent_id = Column(Integer, ForeignKey("recipes.id"))

    title = Column(String)  # Section Header - Shows if Present
    note = Column(String)  # Force Show Text - Overrides Concat

    # Scaling Items
    unit_id = Column(Integer, ForeignKey("ingredient_units.id"))
    unit = orm.relationship(IngredientUnitModel, uselist=False)

    food_id = Column(Integer, ForeignKey("ingredient_foods.id"))
    food = orm.relationship(IngredientFoodModel, uselist=False)
    quantity = Column(Integer)

    reference_id = Column(GUID)  # Reference Links

    @auto_init()
    def __init__(self, **_) -> None:
        pass
