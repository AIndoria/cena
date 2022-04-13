from pydantic import UUID4

from cena.db.models.group.shopping_list import ShoppingList
from cena.schema.group.group_shopping_list import ShoppingListOut, ShoppingListUpdate

from .repository_generic import RepositoryGeneric


class RepositoryShoppingList(RepositoryGeneric[ShoppingListOut, ShoppingList]):
    def update(self, item_id: UUID4, data: ShoppingListUpdate) -> ShoppingListOut:  # type: ignore
        return super().update(item_id, data)
