import pytest

from cena.db.db_setup import SessionLocal
from cena.repos.all_repositories import AllRepositories, get_repositories


@pytest.fixture()
def database() -> AllRepositories:
    try:
        db = SessionLocal()
        yield get_repositories(db)

    finally:
        db.close()
