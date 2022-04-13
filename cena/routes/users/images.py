import shutil
from pathlib import Path

from fastapi import Depends, File, HTTPException, UploadFile, status
from pydantic import UUID4

from cena.core.dependencies.dependencies import temporary_dir
from cena.pkgs import cache, img
from cena.routes._base import BaseUserController, controller
from cena.routes._base.routers import UserAPIRouter
from cena.routes.users._helpers import assert_user_change_allowed
from cena.schema.user import PrivateUser

router = UserAPIRouter(prefix="", tags=["Users: Images"])


@controller(router)
class UserImageController(BaseUserController):
    @router.post("/{id}/image")
    def update_user_image(
        self,
        id: UUID4,
        profile: UploadFile = File(...),
        temp_dir: Path = Depends(temporary_dir),
    ):
        """Updates a User Image"""
        assert_user_change_allowed(id, self.user)
        temp_img = temp_dir.joinpath(profile.filename)

        with temp_img.open("wb") as buffer:
            shutil.copyfileobj(profile.file, buffer)

        image = img.PillowMinifier.to_webp(temp_img)
        dest = PrivateUser.get_directory(id) / "profile.webp"

        shutil.copyfile(image, dest)

        self.repos.users.patch(id, {"cache_key": cache.new_key()})

        if not dest.is_file:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
