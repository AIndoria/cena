from fastapi import APIRouter, Depends, HTTPException, status
from cena.db.database import db
from cena.db.db_setup import generate_session
from cena.routes.deps import get_current_user
from cena.routes.routers import AdminAPIRouter
from cena.schema.settings import SiteSettings
from cena.schema.user import GroupInDB, UserInDB
from cena.utils.post_webhooks import post_webhooks
from sqlalchemy.orm.session import Session

public_router = APIRouter(prefix="/api/site-settings", tags=["Settings"])
admin_router = AdminAPIRouter(prefix="/api/site-settings", tags=["Settings"])


@public_router.get("")
def get_main_settings(session: Session = Depends(generate_session)):
    """ Returns basic site settings """

    return db.settings.get(session, 1)


@admin_router.put("")
def update_settings(
    data: SiteSettings,
    session: Session = Depends(generate_session),
):
    """ Returns Site Settings """
    db.settings.update(session, 1, data.dict())


@admin_router.post("/webhooks/test")
def test_webhooks(
    current_user: UserInDB = Depends(get_current_user),
    session: Session = Depends(generate_session),
):
    """ Run the function to test your webhooks """
    group_entry: GroupInDB = db.groups.get(session, current_user.group, "name")

    try:
        post_webhooks(group_entry.id, session)
    except Exception:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
