from fastapi import Depends
from cena.db.database import db
from cena.db.db_setup import generate_session
from cena.routes.deps import get_current_user
from cena.routes.routers import UserAPIRouter
from cena.schema.shopping_list import ShoppingListIn, ShoppingListOut
from cena.schema.user import UserInDB
from sqlalchemy.orm.session import Session

shopping_list_router = UserAPIRouter(prefix="/api/shopping-lists", tags=["Shopping Lists"])


@shopping_list_router.post("", response_model=ShoppingListOut)
async def create_shopping_list(
    list_in: ShoppingListIn,
    current_user: UserInDB = Depends(get_current_user),
    session: Session = Depends(generate_session),
):
    """ Create Shopping List in the Database """

    list_in.group = current_user.group

    return db.shopping_lists.create(session, list_in)


@shopping_list_router.get("/{id}", response_model=ShoppingListOut)
async def get_shopping_list(id: int, session: Session = Depends(generate_session)):
    """ Get Shopping List from the Database """
    return db.shopping_lists.get(session, id)


@shopping_list_router.put("/{id}", response_model=ShoppingListOut)
async def update_shopping_list(id: int, new_data: ShoppingListIn, session: Session = Depends(generate_session)):
    """ Update Shopping List in the Database """
    return db.shopping_lists.update(session, id, new_data)


@shopping_list_router.delete("/{id}")
async def delete_shopping_list(id: int, session: Session = Depends(generate_session)):
    """ Delete Shopping List from the Database """
    return db.shopping_lists.delete(session, id)
