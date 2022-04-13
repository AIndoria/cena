from datetime import date
from typing import Optional

from pydantic import validator

from cena.schema._cena import CenaModel


class MealIn(CenaModel):
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class MealDayIn(CenaModel):
    date: Optional[date]
    meals: list[MealIn]

    class Config:
        orm_mode = True


class MealDayOut(MealDayIn):
    id: int

    class Config:
        orm_mode = True


class MealPlanIn(CenaModel):
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
    id: int
    shopping_list: Optional[int]

    class Config:
        orm_mode = True
