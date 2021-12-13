from django.conf import settings
from src.additional_settings import cacheops_settings
from django.core.cache import cache
from django.db.models import Subquery, OuterRef
from django.utils import timezone
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import ValidationError
from channels.db import database_sync_to_async

from .models import Chat, Message, UserChat
from main.service import BlogMicroService


class ChatService:
    @staticmethod
    def get_user_chat(user_id: int):
        return Chat.objects.prefetch_related('user_chat').filter(user_chat__user_id=user_id).annotate(
            last_message=Subquery(Message.objects.filter(chat_id=OuterRef('id')).order_by('-date').values('content')
                                  [:1]),
            update_date=Subquery(Message.objects.filter(chat_id=OuterRef('id')).order_by('-date').values('date')
                                 [:1]))

    @staticmethod
    def get_messages(chat_id: str):
        return Message.objects.filter(chat_id=chat_id)

    @staticmethod
    def get_or_set_cache(request, jwt: str):
        cache_key: str = cache.make_key(jwt)
        if cache_key in cache:
            print('in cache',)
            return cache.get(cache_key)
        url = BlogMicroService.reverse_url('chat:user_jwt', )
        print('out cache')
        service = BlogMicroService(url)
        response = service.service_response(data={'jwt': jwt}, method='post')
        if response.status_code != HTTP_200_OK:
            raise ValidationError(response.data)
        cache.set(cache_key, response.data, timeout=60 * 2)
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

    @staticmethod
    def get_or_create_chat(user_1: int, user_2: int):
        queryset = Chat.objects.filter(user_chat__user_id=user_2).filter(user_chat__user_id=user_1)
        if queryset.exists():
            return queryset.first()
        chat = Chat.objects.create(name=f'chat {user_1} + {user_2}')
        users = (
            UserChat(chat=chat, user_id=user_1),
            UserChat(chat=chat, user_id=user_2),
        )
        UserChat.objects.bulk_create(users)
        return chat

    @staticmethod
    def get_user_chat_contacts(user_id: int):
        chats = Chat.objects.prefetch_related('user_chat').filter(user_chat__user_id=user_id)
        return list(UserChat.objects.filter(chat__in=chats).exclude(user_id=user_id).values_list('user_id', flat=True))

    @staticmethod
    def post_users_id(users_id: list):
        user_data: list[dict] = []
        request_users: list[int] = []
        for user_id in users_id:
            cache_key: str = cache.make_key('user', user_id)
            if cache_key in cache:
                user_data.append(cache.get(cache_key))
            else:
                request_users.append(user_id)
        if not request_users:
            return user_data
        url = BlogMicroService.reverse_url('chat:users_id', )
        service = BlogMicroService(url)
        response = service.service_response(data={'users_id': request_users}, method='post')
        for user in response.data:
            cache_key: str = cache.make_key('user', user['id'])
            cache.set(cache_key, user, timeout=120)
            user_data.append(user)
        return user_data


class AsyncChatService:
    @staticmethod
    @database_sync_to_async
    def get_chat_ids(user_id: int):
        return list(Chat.objects.filter(user_chat__user_id=user_id).values_list('id', flat=True))

    @staticmethod
    @database_sync_to_async
    def save_message(user_id: int, message: str, chat_id: str):
        return Message.objects.create(author_id=user_id, content=message, chat_id=chat_id)
