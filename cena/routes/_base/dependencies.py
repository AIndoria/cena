from functools import cached_property
from logging import Logger

from fastapi import Depends
from sqlalchemy.orm import Session

from cena.core.config import get_app_dirs, get_app_settings
from cena.core.dependencies.dependencies import get_admin_user, get_current_user
from cena.core.root_logger import get_logger
from cena.core.settings.directories import AppDirectories
from cena.core.settings.settings import AppSettings
from cena.db.db_setup import generate_session
from cena.lang import Translator, local_provider
from cena.repos import AllRepositories
from cena.schema.user.user import PrivateUser


class SharedDependencies:
    session: Session
    t: Translator
    acting_user: PrivateUser | None

    def __init__(self, session: Session, acting_user: PrivateUser | None, provider: Translator | None = None) -> None:
        self.t = provider or local_provider()
        self.session = session
        self.acting_user = acting_user

    @classmethod
    def public(
        cls,
        session: Session = Depends(generate_session),
        translator: Translator = Depends(local_provider),
    ) -> "SharedDependencies":
        return cls(session, None, translator)

    @classmethod
    def user(
        cls,
        session: Session = Depends(generate_session),
        user: PrivateUser = Depends(get_current_user),
        translator: Translator = Depends(local_provider),
    ) -> "SharedDependencies":
        return cls(session, user, translator)

    @classmethod
    def admin(
        cls,
        session: Session = Depends(generate_session),
        admin: PrivateUser = Depends(get_admin_user),
        translator: Translator = Depends(local_provider),
    ) -> "SharedDependencies":
        return cls(session, admin, translator)

    @cached_property
    def logger(self) -> Logger:
        return get_logger()

    @cached_property
    def settings(self) -> AppSettings:
        return get_app_settings()

    @cached_property
    def folders(self) -> AppDirectories:
        return get_app_dirs()

    @cached_property
    def repos(self) -> AllRepositories:
        return AllRepositories(self.session)
