from datetime import date
from typing import Optional

from fastapi_camelcase import CamelModel
from cena.db.models.mealplan import MealPlan
from pydantic import validator
from pydantic.utils import GetterDict


class MealIn(CamelModel):
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class MealDayIn(CamelModel):
    date: Optional[date]
    meals: list[MealIn]

    class Config:
        orm_mode = True


class MealDayOut(MealDayIn):
    id: int

    class Config:
        orm_mode = True


class MealPlanIn(CamelModel):
    group: str
    start_date: date
    end_date: date
    plan_days: list[MealDayIn]

    @validator("end_date")
    def end_date_after_start_date(v, values, config, field):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("EndDate should be greater than StartDate")
        return v

    class Config:
        orm_mode = True


class MealPlanOut(MealPlanIn):
    uid: int
    shopping_list: Optional[int]

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(_cls, name_orm: MealPlan):
            try:
                return {
                    **GetterDict(name_orm),
                    "group": name_orm.group.name,
                    "shopping_list": name_orm.shopping_list.id,
                }
            except Exception:
                return {
                    **GetterDict(name_orm),
                    "group": name_orm.group.name,
                    "shopping_list": None,
                }
