from aiohttp_session import get_session
from aiohttp.web_exceptions import HTTPUnauthorized

from app.web.app import View

class AuthRequiredMixin(View):
    async def auth (self):
        session = await get_session(self.request)
        if not session:
            raise HTTPUnauthorized
        return None
