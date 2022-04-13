from __future__ import annotations

import enum
from typing import Optional, Union
from uuid import UUID, uuid4

from pydantic import UUID4, Field

from cena.schema._cena import CenaModel
from cena.schema._cena.types import NoneFloat


class UnitFoodBase(CenaModel):
    name: str
    description: str = ""


class CreateIngredientFood(UnitFoodBase):
    label_id: Optional[UUID4] = None


class SaveIngredientFood(CreateIngredientFood):
    group_id: UUID4


class IngredientFood(CreateIngredientFood):
    id: UUID4
    label: Optional[MultiPurposeLabelSummary] = None

    class Config:
        orm_mode = True


class CreateIngredientUnit(UnitFoodBase):
    fraction: bool = True
    abbreviation: str = ""


class SaveIngredientUnit(CreateIngredientUnit):
    group_id: UUID4


class IngredientUnit(CreateIngredientUnit):
    id: UUID4

    class Config:
        orm_mode = True


class RecipeIngredient(CenaModel):
    title: Optional[str]
    note: Optional[str]
    unit: Optional[Union[IngredientUnit, CreateIngredientUnit]]
    food: Optional[Union[IngredientFood, CreateIngredientFood]]
    disable_amount: bool = True
    quantity: float = 1
    original_text: Optional[str]

    # Ref is used as a way to distinguish between an individual ingredient on the frontend
    # It is required for the reorder and section titles to function properly because of how
    # Vue handles reactivity. ref may serve another purpose in the future.
    reference_id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class IngredientConfidence(CenaModel):
    average: NoneFloat = None
    comment: NoneFloat = None
    name: NoneFloat = None
    unit: NoneFloat = None
    quantity: NoneFloat = None
    food: NoneFloat = None


class ParsedIngredient(CenaModel):
    input: Optional[str]
    confidence: IngredientConfidence = IngredientConfidence()
    ingredient: RecipeIngredient


class RegisteredParser(str, enum.Enum):
    nlp = "nlp"
    brute = "brute"


class IngredientsRequest(CenaModel):
    parser: RegisteredParser = RegisteredParser.nlp
    ingredients: list[str]


class IngredientRequest(CenaModel):
    parser: RegisteredParser = RegisteredParser.nlp
    ingredient: str


class MergeFood(CenaModel):
    from_food: UUID4
    to_food: UUID4


class MergeUnit(CenaModel):
    from_unit: UUID4
    to_unit: UUID4


from cena.schema.labels.multi_purpose_label import MultiPurposeLabelSummary

IngredientFood.update_forward_refs()
