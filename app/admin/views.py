from aiohttp_apispec import request_schema
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response
from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest
from aiohttp_session import new_session



class AdminLoginView(View):
    @request_schema(AdminSchema)
    async def post(self):
        data = self.request['data']
        if data["email"] is None:
            raise HTTPBadRequest
        admin = await self.store.admins.get_by_email(data['email'])
        if admin is None:
            raise HTTPForbidden
        session = await new_session(request=self.request)
        admin_json = AdminSchema().dump(admin)
        session['admin'] = admin_json
        return json_response(data=admin_json)


class AdminCurrentView(View):
    async def get(self):
        return json_response(data=AdminSchema().dump(self.request.admin))
