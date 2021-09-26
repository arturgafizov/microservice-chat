from django.conf import settings
from django.db.models import Subquery, OuterRef
from . import models
from .models import Chat, Message


class ChatService:
    @staticmethod
    def get_user_chat(user_id:int):
        return Chat.objects.prefetch_related('user_chat').filter(user_chat__user_id=user_id).annotate(
            last_message=Subquery(Message.objects.filter(chat_id=OuterRef('id')).order_by('-date').values('content')[:1])
        )

    @staticmethod
    def get_messages(chat_id: str):
        return Message.objects.filter(chat_id=chat_id)
