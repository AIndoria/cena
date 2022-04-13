from fastapi import APIRouter, HTTPException, status

from cena.core.config import get_app_settings
from cena.repos.all_repositories import get_repositories
from cena.routes._base import BasePublicController, controller
from cena.schema.response import ErrorResponse
from cena.schema.user.registration import CreateUserRegistration
from cena.schema.user.user import UserOut
from cena.services.user_services.registration_service import RegistrationService

router = APIRouter(prefix="/register")


@controller(router)
class RegistrationController(BasePublicController):
    @router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
    def register_new_user(self, data: CreateUserRegistration):
        settings = get_app_settings()

        if not settings.ALLOW_SIGNUP and data.group_token is None or data.group_token == "":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=ErrorResponse.respond("User Registration is Disabled")
            )

        registration_service = RegistrationService(self.deps.logger, get_repositories(self.deps.session))
        return registration_service.register_user(data)
