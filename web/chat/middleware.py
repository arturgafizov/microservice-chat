from channels.sessions import CookieMiddleware
from .services import ChatService


class CookeAuthMiddlWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        user_jwt = scope['cookies'].get('jwt-auth')
        if not user_jwt:
            return
        # print(user_data)
        scope['user_data'] = ChatService.get_or_set_cache(user_jwt)
        return await self.app(scope, receive, send)


def AuthMiddlewareStack(inner):
    return CookieMiddleware(CookeAuthMiddlWare(inner))
