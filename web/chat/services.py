from django.conf import settings

from . import models
from .models import Chat


class ChatService:
    @staticmethod
    def get_user_chat(user_id:int):
        return Chat.objects.select_related('user_chat').filter(user_chat__user_id=user_id)
