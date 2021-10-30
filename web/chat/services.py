from django.conf import settings
from django.db.models import Subquery, OuterRef
from django.utils import timezone
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import ValidationError

from .models import Chat, Message
from main.service import BlogMicroService


class ChatService:
    @staticmethod
    def get_user_chat(user_id:int):
        return Chat.objects.prefetch_related('user_chat').filter(user_chat__user_id=user_id).annotate(
            last_message=Subquery(Message.objects.filter(chat_id=OuterRef('id')).order_by('-date').values('content')
                                  [:1]),
            update_date=Subquery(Message.objects.filter(chat_id=OuterRef('id')).order_by('-date').values('date')
                                 [:1]))

    @staticmethod
    def get_messages(chat_id: str):
        return Message.objects.filter(chat_id=chat_id)

    @staticmethod
    def post_jwt(request, jwt: str):
        url = BlogMicroService.reverse_url('chat:user_jwt', )
        service = BlogMicroService(request, url)
        print(service.url)
        response = service.service_response(data={'jwt': jwt}, method='post')
        print(response.data, response.status_code)
        if response.status_code != HTTP_200_OK:
            raise ValidationError(response.data)
        return response.data

    @staticmethod
    def set_jwt_access_cookie(response, access_token: str):
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE_NAME', None)
        access_token_expiration = timezone.now() + timezone.timedelta(minutes=settings.JWT_TOKEN_LIFETIME_MIN)
        cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
        cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
        cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')

        if cookie_name:
            response.set_cookie(
                cookie_name,
                access_token,
                expires=access_token_expiration,
                secure=cookie_secure,
                httponly=cookie_httponly,
                samesite=cookie_samesite,
            )
