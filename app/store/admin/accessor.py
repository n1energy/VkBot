import base64
import typing
from hashlib import sha256
from typing import Optional
from gino.api import Gino

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin, AdminModel

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        obj = await AdminModel.query.where(AdminModel.email == email).gino.first()
        if obj is not None:
            return Admin(id=obj.id, email=obj.email, password=obj.password)
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = await self.get_by_email(email)
        if admin is None:
            res = await AdminModel.create(email=email, password=sha256(password.encode()).hexdigest())
            return Admin(**res.to_dict())
        return None
