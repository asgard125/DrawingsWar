from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from game_app.models import User
from django.db import close_old_connections


@database_sync_to_async
def get_user_by_token(token):
    try:
        userid = Token.objects.get(key=token)
        return User.objects.get(pk=userid.user_id)
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes token from the query string.
    """

    async def __call__(self, scope, receive, send):
        close_old_connections()
        scope = dict(scope)
        token = scope["query_string"].decode()
        scope['user'] = await get_user_by_token(token)
        return await super().__call__(scope, receive, send)