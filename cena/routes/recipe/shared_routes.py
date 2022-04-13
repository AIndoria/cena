from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm.session import Session

from cena.db.db_setup import generate_session
from cena.repos.all_repositories import get_repositories
from cena.schema.recipe import Recipe

router = APIRouter()


@router.get("/shared/{token_id}", response_model=Recipe)
def get_shared_recipe(token_id: UUID4, session: Session = Depends(generate_session)):
    db = get_repositories(session)

    token_summary = db.recipe_share_tokens.get_one(token_id)

    if token_summary is None:
        return None

    return token_summary.recipe
