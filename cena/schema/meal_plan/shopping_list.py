from typing import Optional

from pydantic.utils import GetterDict

from cena.db.models.group.shopping_list import ShoppingList
from cena.schema._cena import CenaModel


class ListItem(CenaModel):
    title: Optional[str]
    text: str = ""
    quantity: int = 1
    checked: bool = False

    class Config:
        orm_mode = True


class ShoppingListIn(CenaModel):
    name: str
    group: Optional[str]
    items: list[ListItem]


class ShoppingListOut(ShoppingListIn):
    id: int

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(cls, ormModel: ShoppingList):
            return {
                **GetterDict(ormModel),
                "group": ormModel.group.name,
            }
