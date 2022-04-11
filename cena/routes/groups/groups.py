from fastapi import APIRouter
from cena.routes.groups import crud

router = APIRouter()

router.include_router(crud.admin_router)
router.include_router(crud.user_router)
